from luxon import g
from luxon import register_resource
from luxon.constants import TEXT_PLAIN


@register_resource('GET', '/sitemap')
@register_resource('GET', '/sitemap.txt')
def sitemap(req, resp):
    sitemap = []
    resp.content_type = TEXT_PLAIN
    for route in g.nav_menu._items:
        path_name, view, href, kwargs = route
        if 'http' not in href:
            sitemap.append(req.app_uri + href)
    return "\n".join(sitemap)
