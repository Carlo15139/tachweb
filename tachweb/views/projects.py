import os
import mimetypes
import re

from luxon import register_resource
from luxon import constants as const
from luxon.exceptions import HTTPNotFound
from luxon import render_template
from luxon.constants import TEXT_HTML
from luxon.utils.html import select
from luxon import GetLogger
from luxon.utils.encoding import if_bytes_to_unicode
from luxon import g
from luxon import js

log = GetLogger(__name__)

g.nav_menu.add('/Tachyonic/About',
               href='/rst/tachyonic_project')
g.nav_menu.add('/Tachyonic/Projects',
               href='/projects')
g.nav_menu.add('/Tachyonic/Open Source', href='/rst/opensource')

g.nav_menu.add('/Documentation/Tutorial/Installation',
               href='/rst/installation')                                                                                                    
g.nav_menu.add('/Documentation/Tutorial/Infinitystone Login',
               href='/rst/login_tutorial')
g.nav_menu.add('/Documentation/Tutorial/Deployment',
               href='/rst/deployment')
g.nav_menu.add('/Documentation/Luxon',
               href='/sphinx/luxon')
g.nav_menu.add('/Documentation/Psychokinetic',
               href='/sphinx/psychokinetic')
g.nav_menu.add('/Documentation/Endpoints/InfinityStone',
               href='/sphinx/infinitystone')
g.nav_menu.add('/Documentation/Endpoints/Netrino',
               href='/sphinx/netrino')
g.nav_menu.add('/Documentation/Endpoints/Telepahtic',
               href='/sphinx/telepathic')
g.nav_menu.add('/Documentation/Endpoints/Yoshii',
               href='/sphinx/yoshii')
g.nav_menu.add('/Documentation/Endpoints/Katalog',
               href='/sphinx/katalog')
g.nav_menu.add('/Documentation/Endpoints/Kiloquad',
               href='/sphinx/kiloquad')
g.nav_menu.add('/Documentation/Photonic',
               href='/sphinx/photonic')
g.nav_menu.add('/Documentation/pyipcalc', href='/rst/pyipcalc')
g.nav_menu.add('/Documentation/Development/Blueprints',
               href='/sphinx/blueprints')


def format_body_only(html):
    html = if_bytes_to_unicode(html)
    body_match = re.compile(r"\<!\-\-DOC\-\-\>.*\<\!\-\-DOC\-\-\>",
                            re.IGNORECASE | re.MULTILINE |
                            re.DOTALL)

    for body in body_match.findall(html):
        return body
    return "No content/body"


@register_resource([ 'GET', 'POST' ],
                   'regex:^/sphinx.*$')
def sphinx(req, resp):
    app_root = g.app_root
    full_path = req.relative_resource_uri.strip('/').split('/')[1:]

    if len(full_path) > 0 and full_path[0] in req.context.projects:
        resp.content_type = TEXT_HTML
        name = full_path[0]
        goto = req.get_first('ref')
        if goto is not None:
            return resp.redirect('/sphinx/%s/%s' % (name, goto,))

        project = req.context.projects[name]
        branches = project['branches']
        tags = sorted(project['tags'])
        refs = []
        description = project['description']

        for tag in reversed(tags):
            html_root = app_root + '/docs/%s_%s' % (name, tag,)
            if os.path.exists(html_root):
                refs.append(tag)

        for branch in branches:
            html_root = app_root + '/docs/%s_%s' % (name, branch,)
            if os.path.exists(html_root):
                refs.append(branch)

        if len(refs) == 0:
            raise HTTPNotFound("Project documentation not found")

        if len(full_path) > 1:
            ref = full_path[1]
        else:
            if len(tags) > 0:
                return resp.redirect('/sphinx/%s/%s' % (name, refs[0],))
            else:
                if 'development' in refs:
                    return resp.redirect('/sphinx/%s/development' % name)
                if 'master' in refs:
                    return resp.redirect('/sphinx/%s/master' % name)
            return resp.redirect('/sphinx/%s/%s' % (name, refs[0],))

        doc_path = full_path[2:]

        html_root = app_root + '/docs/%s_%s' % (name, ref)

        if len(doc_path) == 0:
            return resp.redirect('/sphinx/%s/%s/index.html' % (name, ref,))
        else:
            path = "/".join(doc_path)

        path = html_root + '/' + path
        if os.path.isfile(path):
            sfile = open(path, 'rb').read()
            resp.content_type = const.APPLICATION_OCTET_STREAM
            mime_type = mimetypes.guess_type(path)
            if mime_type is not None:
                resp.content_type = mime_type[0]
                if mime_type[1] is not None:
                    resp.content_type += ';charset=%s' % mime_type[1]
            if mime_type[0].lower() == 'text/html':
                refs = select('ref', refs, ref, False, 'select', 'this.form.submit()')
                sfile = format_body_only(sfile)
                return render_template('tachweb/sphinx.html', refs=refs,
                                       doc=sfile, no_news=True,
                                       project=name, title=name,
                                       description=description)
            else:
                return sfile
        else:
            raise HTTPNotFound('Documentation page not found - possibly' +
                               ' updating')

    else:
        raise HTTPNotFound("Project documentation not found")


def projects_docs():
    app_root = g.app_root
    projects = g.current_request.context.projects
    docs = {}
    for project in projects:
        docs[project] = []
        for tag in projects[project]['tags']:
            html_root = app_root + '/docs/%s_%s' % (project, tag,)
            if os.path.exists(html_root):
                docs[project].append(tag)

        for branch in projects[project]['branches']:
            html_root = app_root + '/docs/%s_%s' % (project, branch,)
            if os.path.exists(html_root):
                docs[project].append(branch)

        docs[project] = sorted(docs[project])

    return docs

@register_resource('GET',
                   '/projects')
def projects(req, resp):
    resp.content_type = TEXT_HTML
    rst = render_template('tachweb/projects.rst', rst2html=True)
    projects = req.context.projects
    projects_sorted = sorted(projects.keys())
    versions = {}
    docs = projects_docs()
    for project in projects:
        versions[project] = []
        for tag in projects[project]['tags']:
            versions[project].append(tag)

        for branch in projects[project]['branches']:
            versions[project].append(branch)

        versions[project] = ", ".join(sorted(versions[project]))

    return render_template('tachweb/projects.html',
                           projects=projects,
                           projects_sorted=projects_sorted,
                           versions=versions,
                           docs=docs,
                           rst=rst)

@register_resource('GET',
                   '/project/{project}')
def project(req, resp, project):
    resp.content_type = TEXT_HTML
    project = req.context.projects[project]
    return render_template('tachweb/project.html', project=project)
