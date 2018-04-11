import operator
from luxon.utils.objects import load
from luxon import g


class GitHub(object):
    def pre(self, req, resp):
        app = g.app_root
        planning = load(app + '/planning.pickle')
        projects = load(app + '/projects.pickle')
        req.context.planning = planning
        req.context.projects = projects

        all_news = []
        for project in projects:
            all_news += projects[project]['events']

        news = []
        for item in sorted(all_news, key=operator.itemgetter(0)):
            news.append(item)
        news = req.context.news = list(reversed(news))
