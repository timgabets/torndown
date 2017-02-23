# Torndown 
Tornado web plugin to generate pages from Markdown.
Markdown may be stored in a foreign repository for high flexability and control.

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
import torndown
import tornado.web
import tornado.ioloop
import tornado.httpclient

# Repository
os.environ["TORNDOWN_REPO"] = "stevepeak/torndown"
# The template to insert the rendered markdown
os.environ["TORNDOWN_TEMPLATE"] = "../example/base.html"

application = tornado.web.Application([
  # !important to have the r"(.*)"
  (r"/(.*)", torndown.TorndownHandler)
])

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
