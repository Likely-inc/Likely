import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os
import json
from InstaAPI import instagramConnectionFacade
from platform import system
import learner as lrn

ipAndCodes = dict()
ipAndInfo = dict()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("src/index.html")

class ResultHandler(tornado.web.RequestHandler):
    def get(self):
        t = ipAndCodes[self.request.remote_ip]
        d = ipAndInfo[self.request.remote_ip]
        statuses = [("1",10),("2",15),("3",11),("4",29),("5",12),("6",10),("7",35),("8",30),("9",32),("10",30)]
        s = self.parseResults(statuses)
        self.render("src/LikelyResults.html", nLikes=d["likes"], iPath=d["path"],
                    uName=t.getUser(), pProfile=t.getProfilePic(),
                    caption=d["caption"], hour_likes=s)
    def parseResults(self, l):
        l.sort(key=lambda x: x[1], reverse=True)
        newL = []
        maxV = l[0][1]
        for elem in l:
            newL.append((elem[0], elem[1], int((elem[1] / maxV) * 100)))
        newL.sort(key=lambda x: int(x[0]))
        return newL


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Restart the server 3")
        print("Killing python")
        os.system("./PullScriptForOmer")


class AppHandler(tornado.web.RequestHandler):
    def get(self):

        t = instagramConnectionFacade(self.get_argument("code"),"5f46ab2c0ce24bdaa966b3ea9b1b9b2a", "8c5523d19c604c0dac2c66946083a5b4",
                                      "http://ec2-54-244-111-228.us-west-2.compute.amazonaws.com/app")
        ipAndCodes[self.request.remote_ip] = t
        self.render("src/LikelyMain.html", uname=t.getUser(), pProfile=t.getProfilePic())

class UploadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def post(self):
        file1 = self.request.files['filearg'][0]
        comment = self.request.body_arguments["captionarg"][0].decode()
        original_fname = file1['filename']
        t = ipAndCodes[self.request.remote_ip]
        path = "src/upload/%s/%s" %(t.getUser(),original_fname)
        if not os.path.exists("src/upload/"+t.getUser()):
            os.makedirs("src/upload/"+t.getUser())
        output_file = open(path, 'wb+')
        output_file.write(file1['body'])
        likes = lrn.train(t.getRecentPhotos(1000),[path,comment])
        ipAndInfo[self.request.remote_ip] = {"likes":likes,
                                             "path":"upload/"+t.getUser()+"/"+original_fname,
                                             "caption":comment}
        self.redirect("/results")





class Application(tornado.web.Application):
    code = None
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
            (r"/results", ResultHandler),
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
    print("The server is UP and running")
    tornado.ioloop.IOLoop.current().start()

