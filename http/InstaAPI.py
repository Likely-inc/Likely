import requests
import json
user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
headers = {'User-Agent': user_agent,
           "Content-type": "application/x-www-form-urlencoded"
           }

class instagramConnectionFacade:
    __api = None
    __uName = None
    __aToken = None
    __pPicture = None
    __uId = None
    def __init__(self, client_id, appId, appSecret, URI):
        url = "https://api.instagram.com/oauth/access_token"
        values = {
            'client_id':appId,
            'client_secret':appSecret,
            'grant_type':'authorization_code',
            'redirect_uri':URI,
            'code':client_id
        }
        try:
            r = requests.post(url, data=values)
            js = json.loads(r.text)
            self.__aToken = js["access_token"]
            js = js["user"]
            self.__uName = js["username"]
            self.__pPicture = js["profile_picture"]
            self.__uId = js["id"]
        except Exception as e:
            print(e.args)

    def getUser(self):
        return self.__uName

    def getProfilePic(self):
        return self.__pPicture

    def parseMedia(self, js, count):
        l = []
        print(json.dumps(js))
        js = js["data"]
        try:
            for elem in js[:count-1]:
                print("======================")
                print(elem)
                print("=======-----===============")
                if(elem["type"] == "video"):
                    continue
                d = dict()
                print("V likes")
                d["likes"] = elem["likes"]["count"]
                print("V created time")
                d["created_time"] = elem["created_time"]
                print("V image ling")
                d["image_link"] = elem["images"]["standard_resolution"]["url"]
                print("V filter")
                d["filter"] = elem["filter"]
                print("V location")
                if(elem["location"] == None):
                    d["location"] = "Not exists"
                else:
                    d["location"] = elem["location"]["name"]
                print("V caption")
                if (elem["caption"] == None):
                    d["caption"] = "Not exists"
                else:
                    d["caption"] = elem["caption"]["text"]
                l.append(d)
                print(d)
        except Exception as e:
            print(e.args)
        return l

    def getRecentPhotos(self,count):
        url = "https://api.instagram.com/v1/users/self/media/recent/?access_token=%s"%(self.__aToken)
        values = {
            'count':str(count),
        }
        try:
            r = requests.get(url,params=values)
            js = json.loads(r.text)
            return self.parseMedia(js, count)
        except Exception as e:
            print(e.args)



