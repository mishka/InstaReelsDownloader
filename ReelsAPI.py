from instagrapi import Client

class Insta:
    def __init__(self):
        self.gram = Client()

    def VideoURL(self, url):
        fetch_id = self.gram.media_pk_from_url(url)
        info = self.gram.media_info(fetch_id).dict()
        return info['video_url']


#print(Insta().VideoURL('https://www.instagram.com/p/CbiU611JZ3i/'))
