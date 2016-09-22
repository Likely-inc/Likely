

from instagram.client import InstagramAPI
class instagramConnectionFacade:
    __api = None
    def __init__(self, client_id, appId, appSecret, URI):
        self.__api = InstagramAPI(
            client_id=appId,
            client_secret=appSecret,
            redirect_uri=URI, access_token=URI)

    def getUser(self):
        return self.__api.user
