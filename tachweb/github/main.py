#!/usr/bin/python3
import os
import subprocess
import argparse
import sys
from string import Template
from time import sleep
from pkg_resources import resource_stream
import site
import traceback

from luxon.utils.encoding import if_bytes_to_unicode
from luxon.utils.objects import save, load
from luxon import Config
from luxon.utils.python import create_env
from psychokinetic.github import GitHub
from luxon import GetLogger
from luxon import g
from luxon import send_email
from luxon.utils.objects import object_name
from luxon.utils.daemon import Daemon

log = GetLogger()


def execute(*args):
    completed = subprocess.run(*args, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               check=True)
    log.info(completed.stdout)


def build_doc(root_path, venv_path, src_path, ref, doc_dir, name):
    os.chdir(src_path)
    log.info("Checkout '%s/%s'" % (name, ref,))
    execute(["git", "checkout", ref])
    metadata_py = src_path + '/' + name + '/metadata.py'
    exec_globals = {}
    exec(open(metadata_py).read(), exec_globals, exec_globals)

    confpy = venv_path + '/conf.py'
    if os.path.exists(confpy):
        os.remove(confpy)
    with resource_stream('tachweb', 'github/conf.py.tpl') as tpl_file:
        template = Template(if_bytes_to_unicode(tpl_file.read()))
    with open(confpy, 'w') as real_file:
        real_file.write(template.safe_substitute(
            **exec_globals))

    buildsh = venv_path + '/build.sh'
    if os.path.exists(buildsh):
        os.remove(buildsh)
    with resource_stream('tachweb', 'github/build.sh.tpl') as tpl_file:
        template = Template(if_bytes_to_unicode(tpl_file.read()))
    with open(buildsh, 'w') as real_file:
        real_file.write(template.safe_substitute(
            virtualenv=venv_path,
            src_path=src_path,
            doc_dir=doc_dir))

    os.chmod(buildsh, 0o700)

    execute(["/usr/bin/env",
            venv_path + "/build.sh",
            venv_path,
            src_path,
            doc_dir])


def clone(clone_url, dest):
    execute(["git", "clone", clone_url, dest])


def daemon(root_path, config):
    try:
        projects = load(root_path + '/projects.pickle')
    except FileNotFoundError:
        projects = {}

    email = config.get('github', 'email')
    rcpt = config.get('github', 'rcpt')
    username = config.get('github', 'username')
    password = config.get('github', 'password')

    tachyonic = GitHub('https://api.github.com',
                       auth=(username, password))

    while True:
        try:
            save(tachyonic.projects('TachyonicProject'),
                 root_path + '/planning.pickle')
            found = []
            log.info("Getting Repos")
            repos = tachyonic.repos('TachyonicProject')
            for repo in repos:
                name = repo['name']
                found.append(name)
                description = repo['description']
                if name not in projects:
                    projects[name] = {}
                log.info("Scanning Repo " + name)
                updated_at = repo['updated_at']
                created_at = repo['updated_at']
                projects[name]['description'] = description
                projects[name]['created_at'] = created_at
                projects[name]['events'] = tachyonic.events('TachyonicProject',
                                                            name)
                if (name in projects and
                        'updated_at' in projects[name] and
                        updated_at == projects[name]['updated_at']):
                    log.info("Already up-to-date (%s)" % updated_at)
                    continue

                projects[name]['updated_at'] = updated_at

                clone_url = repo['clone_url']
                projects[name]['clone_url'] = clone_url
                log.info("Getting Branches for %s" % name)
                branches = tachyonic.branches('TachyonicProject', name)
                log.info("Getting Tags for %s" % name)
                tags = tachyonic.tags('TachyonicProject', name)
                refs = branches + tags
                projects[name]['refs'] = refs
                projects[name]['branches'] = branches
                projects[name]['tags'] = tags
                projects[name]['doc_refs'] = {}
                for ref in refs:
                    venv_dir = "%s/github/%s_%s" % (root_path, name, ref,)
                    doc_dir = "%s/docs/%s_%s" % (root_path, name, ref,)
                    src_path = venv_dir + '/' + name
                    log.info("Creating Virtual Environment '%s'" % venv_dir)
                    create_env(venv_dir, wipe=True, site_packages=True)
                    clone(clone_url, src_path)
                    if (os.path.exists(src_path + '/docs/source/conf.py') and
                            os.path.exists(src_path + '/docs/Makefile')):
                        log.info("Bulding '%s' ref '%s'" % (name, ref,))
                        projects[name]['doc_refs'][ref] = True
                        build_doc(root_path, venv_dir,
                                  src_path, ref,
                                  doc_dir, name)
                    else:
                        projects[name]['doc_refs'][ref] = False
                        log.warning("No Sphinx docs found ref '%s'" % ref)

                save(projects, root_path + '/projects.pickle')

            for pj in projects:
                if pj not in found:
                    del projects[pj]
            save(projects, root_path + '/projects.pickle')
            log.info('Infinite loop sleeping 121 seconds')
            sleep(121)

        except KeyboardInterrupt:
            print("Control-C closed / Killed")
            break
        except Exception as e:
            trace = str(traceback.format_exc())
            error = '%s: %s' % (object_name(e),
                                e)

            try:
                if e.status == 401:
                    if log.debug_mode():
                        log.debug(trace)
                    else:
                        log.error(error)

                    send_email(email, rcpt,
                               subject='GitHub TachWeb Error %s' % error,
                               body=trace)
                    break
                log.error(e)
            except AttributeError:
                if log.debug_mode():
                    log.debug(trace)
                else:
                    log.error(error)

            send_email(email, rcpt,
                       subject='GitHub TachWeb Error %s' % error,
                       body=trace)
            log.info('Error in loop sleeping 5 minutes')
            sleep(300)


def main(argv):
    try:
        parser = argparse.ArgumentParser()
        action = parser.add_mutually_exclusive_group()
        parser.add_argument('path',
                            help='Tachyonic Web Location')
        action.add_argument('-s', '--start',
                            action='store_true',
                            help='Fork Process')
        parser.add_argument('-f', '--fork',
                            action='store_true',
                            help='Fork Process')
        action.add_argument('-k', '--kill',
                            action='store_true',
                            help='Stop/Kill Process')
        action.add_argument('-r', '--restart',
                            action='store_true',
                            help='Restart Process')

        args = parser.parse_args()
        root_path = os.path.abspath(os.path.abspath(args.path))
        pid_file = root_path + '/github.pid'
        config = g.config = Config()
        config.load(root_path + '/settings.ini')
        GetLogger().app_configure()

        site.addsitedir(os.path.abspath(root_path))

        def proc():
            daemon(root_path, config)

        fork = Daemon(pid_file, run=proc)

        if args.start:
            if args.fork is True:
                fork.start()
            else:
                fork.start(fork=False)
        else:
            if args.kill is True:
                fork.stop()
            if args.restart is True:
                fork.restart()

    except KeyboardInterrupt:
        print("Control-C closed / Killed")


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
