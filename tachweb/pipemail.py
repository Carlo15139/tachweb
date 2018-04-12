#!/usr/bin/python3
import sys
import email

from luxon import g
from luxon import Config
from luxon import GetLogger
from luxon import send_email
from luxon import db
from luxon.utils.mail import format_msg

log = GetLogger()

html_template = """
Greetings {{name}}

{{body}}

You can unsubscribe here: http://www.tachyonic.org/unsubscribe/{{token}}
"""

text_template = """
Greetings {{name}}

{{body}}

You can unsubscribe here: http://www.tachyonic.org/unsubscribe/{{token}}
"""

def main(argv):
    config = g.config = Config()
    config.load('/var/www/tachweb/settings.ini')
    GetLogger().app_configure()
    msg = sys.stdin.read()
    msg = email.message_from_string(msg)
    with db() as conn:
        cursor = conn.execute('SELECT * FROM newslist')
        for rcpt in cursor:
            to = "%s <%s>" % (rcpt['name'], rcpt['email'],)
            new = format_msg(msg,
                       html_template=html_template,
                       text_template=text_template,
                       email_from='no-reply@tachyonic.org',
                       email_to=to,
                       multipart=True,
                       test=None)
            try:
                send_email('no-reply@tachyonic.org', to, msg=new)
            except Exception as e:
                log.critical('Failed to send to %s (%s)' % (rcpt, e,))

def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
