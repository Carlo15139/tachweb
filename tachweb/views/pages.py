import re
from docutils.core import publish_string

from luxon import g
from luxon import GetLogger
from luxon import render_template
from luxon import register_resource
from luxon.utils.encoding import if_bytes_to_unicode
from luxon.constants import TEXT_HTML

log = GetLogger(__name__)

g.nav_menu.add('/Community/Sponsors', href='/rst/project_sponsors')
g.nav_menu.add('/Community/Get involved', href='/rst/get_involved')


@register_resource('GET', '/pyipcalc')
def pyipcalc(req, resp):
    resp.redirect('/rst/pyipcalc')


@register_resource('GET', '/rst/{page}')
def pages(req, resp, page):
    resp.content_type = TEXT_HTML
    content = render_template("tachweb/%s.rst" % (page,), rst2html=True)
    title = page.replace('_', ' ').title()
    return render_template('tachweb/pages.html', title=title, content=content)


@register_resource('GET', '/')
def home(req, resp):
    resp.redirect('/rst/tachyonic_project')

