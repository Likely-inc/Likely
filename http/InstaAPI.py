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
        js = js["data"]
        try:
            for elem in js:
                if(elem["type"] == "video"):
                    continue
                d = dict()
                d["likes"] = elem["likes"]["count"]
                d["created_time"] = elem["created_time"]
                d["image_link"] = elem["images"]["low_resolution"]["url"]
                d["filter"] = elem["filter"]
                d["id"] = elem["id"]
                if(elem["location"] == None):
                    d["location"] = "Not exists"
                else:
                    d["location"] = elem["location"]["name"]
                if (elem["caption"] == None):
                    d["caption"] = "Not exists"
                else:
                    d["caption"] = elem["caption"]["text"]
                l.append(d)
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



