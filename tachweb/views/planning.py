from luxon import register_resource
from luxon import render_template
from luxon.constants import TEXT_HTML
from luxon import g

g.nav_menu.add('/Tachyonic/Planning',
               href='/planning')


@register_resource('GET',
                   '/planning')
def planning(req, resp):
    resp.content_type = TEXT_HTML
    return render_template('tachweb/planning.html')
