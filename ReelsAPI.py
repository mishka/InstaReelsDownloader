from instagrapi import Client
from instagrapi import exceptions

class LoginError(Exception):
    pass

class Insta:
    def __init__(self):
        self.gram = Client()

    def VideoURL(self, url):
        try:
            fetch_id = self.gram.media_pk_from_url(url)
            info = self.gram.media_info_a1(fetch_id).dict()
            return info['video_url']
        except exceptions.LoginRequired:
            raise LoginError('Sorry, can\'t access this post without logging in.')
