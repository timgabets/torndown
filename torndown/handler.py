import re
import debris
import markdown2
import tornado.web
import tornado.gen
import tornado.escape
import tornado.httpclient
from tornado.httputil import url_concat
from base64 import b64decode as decode

from . import version


class TorndownHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, path):
        """Example route:
        (r"/some/base/path/(.*)", torndown.TorndownHandler)

        TORNDOWN_REPO := "owner/repo#ref" ex. "stevepeak/torndown#master"
        ... note: `ref` defaults to the repository's default branch (usually `master`)
        """
        path = re.sub(r'^\/*', '', path)
        path = re.sub(r'\/*$', '', path)
        for setting in ('TORNDOWN_REPO', 'TORNDOWN_ACCESS_TOKEN', 'TORNDOWN_TEMPLATE'):
            self.require_setting(setting, "Torndown Rendering")

        # cache = yield debris.locale.memory.get(path)
        cache = debris.locale.memory.get(path)
        if cache:
            self.render(self.settings['TORNDOWN_TEMPLATE'], torndown=cache)

        else:
            # Build arguments to get the markdown
            url = "https://api.github.com/repos/%s/contents/%s.md"
            repo = self.settings['TORNDOWN_REP'].split('#')
            headers = {'User-Agent': 'Torndown v%s' % version}
            urlargs = {}
            if 'TORNDOWN_ACCESS_TOKEN' in self.settings and self.settings['TORNDOWN_ACCESS_TOKEN']:
                urlargs['access_token'] = self.settings['TORNDOWN_ACCESS_TOKEN']
            if len(repo) is 2:
                urlargs['ref'] = repo[1]

            http_client = tornado.httpclient.AsyncHTTPClient()
            # Yield the markdown content from Github API v3
            response = yield http_client.fetch(url_concat(url % (repo[0], path), urlargs), headers=headers)

            if response.code is 200:
                body = tornado.escape.json_decode(response.body)
                if body['message'] == "Not Found":
                    # the file was not found, lets try to see if there is an index file...
                    response = yield http_client.fetch(url_concat(url % (repo[0]+'/index', path), urlargs), headers=headers)
                    body = tornado.escape.json_decode(response.body)
                if body['message'] == "Not Found":
                    raise tornado.web.HTTPError(404)
                elif 'content' in body:
                    try:
                        content = markdown2.markdown(decode(body['content']))
                        # yield debris.locale.memory.set(path, content)
                        debris.locale.memory.set(path, content)
                        self.render(self.settings['TORNDOWN_TEMPLATE'],
                                    torndown=content)
                    except:
                        raise tornado.web.HTTPError(response.code)
                else:
                    raise tornado.web.HTTPError(400, body['message'])
            else:
                raise tornado.web.HTTPError(404)

class TorndownGithubHandler(tornado.web.RequestHandler):
    def post(self):
        """Handles the Github hook to re-process templates
        """
        pass
