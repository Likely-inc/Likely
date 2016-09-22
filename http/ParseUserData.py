import instagram.oauth2
from instagram.client import InstagramAPI
class moshe:
    __api = None
    def __init__(self, userId, appId):
        self.__api = InstagramAPI(userId=userId)

    def getRecentMedia(self):
        return self.__api.user_recent_media(self.__api.user, count=10)
