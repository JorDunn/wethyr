# -*- coding: utf-8 -*-
#!/usr/bin/env python

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from wethyr import app

wethyr_app = WSGIContainer(app)

application = Application([
	(r".*", FallbackHandler, dict(fallback=wethyr_app)),
])

if __name__ == "__main__":
	application.listen(5000)
	IOLoop.instance().start()