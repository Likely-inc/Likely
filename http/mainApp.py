import tornado.ioloop
import tornado.web
import tornado.auth
import os.path
from instagram.client import InstagramAPI
from InstaAPI import instagramConnectionFacade
from platform import system


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("src/index.html")

class AppHandler(tornado.web.RequestHandler):
    def get(self):
        t = instagramConnectionFacade(self.get_argument("code"),"5f46ab2c0ce24bdaa966b3ea9b1b9b2a", "8c5523d19c604c0dac2c66946083a5b4",
                                      self.get_argument("Host")+"/app")
        user = t.getUser()
        print(user)




class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "src")
        }
        handlers = [
            (r"/", MainHandler),
            (r"/auth", AppHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def make_app():
    return Application()

if __name__ == "__main__":
    if system() == "Windows":
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

