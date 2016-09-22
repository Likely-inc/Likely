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
            self.__uName = js["full_name"]
            self.__pPicture = js["profile_picture"]
            self.__uId = js["id"]
        except Exception as e:
            print(e.args)

    def getUser(self):
        return self.__uName

    def getProfilePic(self):
        return self.__pPicture


    def getRecentPhotos(self,count):
        url = "https://api.instagram.com/v1/media/shortcode/D?access_token=%s"%(self.__aToken)
        values = {
            'count':str(count),
        }
        try:
            print(url, values)
            r = requests.post(url, data=values)
            print("HEY")
            print(r.text[:300])
            # js = json.loads(r.text)
            # print(js)
        except Exception as e:
            print(e.args)

