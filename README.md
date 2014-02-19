# Torndown [![Build Status](https://secure.travis-ci.org/stevepeak/torndown.png)](http://travis-ci.org/stevepeak/torndown) [![Version](https://pypip.in/v/torndown/badge.png)](https://github.com/stevepeak/torndown)

> Inspiration credited to [Scalling Asana.com][3]

## Features
- Request handler plugin for [Tornado Web][1]
- Github Integration by storing you markdown in a seperate repository
- Renders static [markdown][2] pages
- Caches page build for speed via [Debris][4]

## Install
`pip install torndown`

## Usage

```python
import os
import tornado.web
import tornado.ioloop
import tornado.httpclient

import torndown

application = tornado.web.Application([
    (r"/(.*)", torndown.TorndownHandler) # !important to have the r"(.*)"
  ],
  TORNDOWN_REPO="stevepeak/torndown#master", # Github repository w/ reference
  TORNDOWN_TEMPLATE="../example/base.html") # The template to insert the rendered markdown

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
```

### Real world example

Your support documentation, about us, home page copy and more can be stores in markdown files
in a seperate repository. There are many advantages to this. To learn more please read this
[great article by Justin Krause at Asana][3] which describes *pretty much* exactly what
`Torndown` can do for your website.

[1]: http://www.tornadoweb.org/
[2]: http://daringfireball.net/projects/markdown/
[3]: http://eng.asana.com/2014/02/scaling-asana-com/
[4]: https://github.com/stevepeak/debris
