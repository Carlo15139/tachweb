#!/usr/bin/python3
import os
import sys
import email

from luxon import g
from luxon import Config
from luxon import GetLogger
from luxon import send_email
from luxon import db
from luxon.utils.mail import format_msg

log = GetLogger()

# WHEN WE RECEIVE HTML MESSAGE WE PARSE IT WITH THIS TEMPLATE JINJA
html_template = """
<html>
<body>
Greetings {% if name %} {{name}} {% endif %}

{{body}}

You can unsubscribe by using this link:
http://www.tachyonic.org/unsubscribe/{{token}}<BR>

<A HREF="http://www.tachyonic.org/unsubscribe/{{token}}">Click Here to unsubscribe</A>

</body>
</html>
"""

# WHEN WE RECEIVE TEXT OR BOTH TEXT AND HTML WE PARSE THE TEXT PORITIONS WITH
# THIS TEMPLATE. HOWERVER IF WE DID NOT GET INCLUDED FOR BACKWARDS COMPATIBILITY
# WE WILL CREATE THE TEXT AND PARSE IT WITH THIS.
text_template = """
Greetings {% if name %} {{name}} {% endif %}

{{body}}

You can unsubscribe here: http://www.tachyonic.org/unsubscribe/{{token}}
"""

def main(argv):
    # PLEASE STICK WITH THIS - ITS MORE SECURE
    unix_user = pwd.getpwuid(os.getuid())[0]
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
                       token=rcpt['token'],
                       name=rcpt['name'])
            try:
                send_email('no-reply@tachyonic.org', to, msg=new)
            except Exception as e:
                log.critical('Failed to send to %s (%s)' % (rcpt, e,))

def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
