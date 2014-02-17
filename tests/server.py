import tornado.ioloop
import tornado.web
import tornado.httpclient
import os

import torndown

application = tornado.web.Application([(r"/", torndown.TorndownHandler)],
                                      TORNDOWN_REPO="stevepeak/torndown",
                                      TORNDOWN_TEMPLATE="../example/base.html")

if __name__ == '__main__':
    application.listen(int(os.getenv('PORT', 5000)))
    tornado.ioloop.IOLoop.instance().start()
