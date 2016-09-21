import tornado.ioloop
import tornado.web
import os.path


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render_string("src/index.html")

class AppHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world2")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/app", AppHandler)
        ]
        settings = {
            "debug": True,
            # "static_path": os.path.join(os.path.dirname(__file__), "src")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def make_app():
    return Application()

if __name__ == "__main__":
    http_server = Application()
    http_server.listen(80)
    tornado.ioloop.IOLoop.current().start()

