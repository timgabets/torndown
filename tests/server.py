import os
import tornado.web
import tornado.ioloop
import tornado.autoreload
import tornado.httpclient

import torndown

# Set this settings in your environment file.
os.environ["TORNDOWN_REPO"] = "stevepeak/torndown"
os.environ["TORNDOWN_TEMPLATE"] = "../example/base.html"
# os.environ["TORNDOWN_STORAGE"] = "memory"
# os.environ["TORNDOWN_EXPIRES"] = ""
# os.environ["TORNDOWN_ACCESS_TOKEN"] = ""

application = tornado.web.Application([(r"/(.*)", torndown.TorndownHandler)],
                                      autoreload=True, debug=True)

if __name__ == '__main__':
    application.listen(int(os.getenv('PORT', 8888)))
    tornado.ioloop.IOLoop.instance().start()
