import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os
import json
from InstaAPI import instagramConnectionFacade
from platform import system


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("src/index.html")


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Restart the server 3")
        print("Killing python")
        os.system("./PullScriptForOmer")


class AppHandler(tornado.web.RequestHandler):
    def get(self):
        t = instagramConnectionFacade(self.get_argument("code"),"5f46ab2c0ce24bdaa966b3ea9b1b9b2a", "8c5523d19c604c0dac2c66946083a5b4",
                                      "http://ec2-54-244-111-228.us-west-2.compute.amazonaws.com/app")
        l = t.getRecentPhotos(5)
        print("The photos are")
        print(l)
        self.render("src/LikelyMain.html", uname=t.getUser(), pProfile=t.getProfilePic())

class UploadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def post(self):
        file1 = self.request.files['filearg'][0]
        comment = self.request.body_arguments
        print(comment)
        original_fname = file1['filename']

        output_file = open("upload/" + original_fname, 'wb+')
        output_file.write(file1['body'])

        self.finish("file " + original_fname + " is uploaded")




class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "src")
        }
        handlers = [
            (r"/", MainHandler),
            (r"/app", AppHandler),
            (r"/upload", UploadHandler),
            (r"/reset", ResetHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def make_app():
    return Application()

if __name__ == "__main__":
    if system() in ["Windows", "Darwin"]:
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

