import tornado.ioloop
import tornado.web
import tornado.auth
import os.path
from instagram.client import InstagramAPI
from ParseUserData import moshe


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("src/index.html")

class AppHandler(tornado.web.RequestHandler):
    def get(self):
        t = moshe(self.get_argument("code"),"5f46ab2c0ce24bdaa966b3ea9b1b9b2a")
        rMedia, next_ = t.getRecentMedia()
        for m in rMedia:
            self.write(m.caption.text)
        self.write(t)




class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "src")
        }
        handlers = [
            (r"/", MainHandler),
            (r"/app", AppHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def make_app():
    return Application()

if __name__ == "__main__":
    http_server = Application()
    http_server.listen(80)
    tornado.ioloop.IOLoop.current().start()

