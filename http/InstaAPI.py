

from instagram.client import InstagramAPI
from instagram.oauth2 import OAuth2AuthExchangeRequest
import urllib,json
user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
headers = {'User-Agent': user_agent,
           "Content-type": "application/x-www-form-urlencoded"
           }

class instagramConnectionFacade:
    __api = None
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
            print("Hey")
            data = urllib.urlencode(values)
            req = urllib.Request(url, data, headers)
            response = urllib.urlopen(req)
            result = response.read()
            dataObj = json.loads(result)
            print(dataObj)
            print("Boom")
        except Exception as e:
            print(e.args)
        # self.__api = InstagramAPI(
        #     client_id=appId,
        #     client_secret=appSecret,
        #     redirect_uri=URI, access_token=client_id)

    def getUser(self):
        popular_media = self.__api.media_popular(count=20)
        return [elem.images['standard_resolution'].url for elem in popular_media]
