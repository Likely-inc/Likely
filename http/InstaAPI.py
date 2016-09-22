

from instagram.client import InstagramAPI
class instagramConnectionFacade:
    __api = None
    def __init__(self, client_id, appId, appSecret, URI):
        self.__api = InstagramAPI(
            client_id=appId,
            client_secret=appSecret,
            redirect_uri=URI, access_token=client_id)

    def getUser(self):
        popular_media = self.__api.media_popular(count=20)
        return [elem.images['standard_resolution'].url for elem in popular_media]
