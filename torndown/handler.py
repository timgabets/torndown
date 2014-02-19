import os
import re
import debris
import markdown2
import tornado.web
import tornado.gen
import tornado.escape
import tornado.httpclient
from tornado.httputil import url_concat
from base64 import b64decode as decode

from torndown import version


class TorndownHandler(tornado.web.RequestHandler):
    def initialize(self):
        storage = os.getenv('TORNDOWN_STORAGE', 'memory')
        self._torndown_storage = debris.storage.use(storage)
        self._torndown_storage.default(expires=os.getenv('TORNDOWN_EXPIRES'))

    @tornado.gen.coroutine
    def get(self, path):
        """Example route:
        (r"/some/base/path/(.*)", torndown.TorndownHandler)

        TORNDOWN_REPO := "owner/repo#ref" ex. "stevepeak/torndown#master"
        ... note: `ref` defaults to the repository's default branch (usually `master`)
        """

        # fix path by replacing extra "/"s
        path = re.sub(r'^\/*', '', path)
        path = re.sub(r'\/*$', '', path)

        cache = self._torndown_storage.get("torndown:"+path)
        template = os.getenv('TORNDOWN_TEMPLATE')
        
        if cache:
            # the markdown was found in cache
            if template:
                self.render(template, torndown=cache)
            else:
                self.finish(cache)

        else:
            # Build arguments to get the markdown
            uri = "https://api.github.com/repos/%s/contents/%s.md"
            repo = os.getenv('TORNDOWN_REPO').split('#')
            headers = {'User-Agent': 'Torndown v%s' % version}
            urlargs = {}
            access_token = os.getenv('TORNDOWN_ACCESS_TOKEN')
            if access_token:
                urlargs['access_token'] = access_token

            if len(repo) is 2:
                urlargs['ref'] = repo[1]

            url = url_concat(uri % (repo[0], path), urlargs)
            
            # Yield the markdown content from Github API v3
            http_client = tornado.httpclient.AsyncHTTPClient()
            response = None
            try:
                response = yield http_client.fetch(url, headers=headers)

            except tornado.httpclient.HTTPError as error:
                if str(error.code) == "404":
                    # the file was not found, lets try to see if there is an index file...
                    url = url_concat(uri % (repo[0], path+'/index'), urlargs)
                    response = yield http_client.fetch(url, headers=headers)
                    # we can allow this to throw a http error's
                else:
                    raise

            finally:
                if response:
                    # debode the api body
                    body = tornado.escape.json_decode(response.body)

                    if 'content' in body:
                        try:
                            # parse the markdown
                            content = markdown2.markdown(decode(body['content']))
                            # store the cache
                            self._torndown_storage.set("torndown:"+path, content)
                            # build the template
                            self.render(template, torndown=content)
                        except:
                            raise tornado.web.HTTPError(response.code)

                    else:
                        raise tornado.web.HTTPError(response.code, body['message'])

                else:
                    raise tornado.web.HTTPError(404)
