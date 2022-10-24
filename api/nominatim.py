import requests


class NominatimAPI:
    def __init__(self):
        self.url = 'https://nominatim.openstreetmap.org'
        self.headers = {'accept-language': 'ru,en;q=0.9'}
        self.session = requests.Session()

    def search(self, params):
        return self.session.get(url=self.url + '/search', headers=self.headers, params=params)

    def reverse(self, params):
        return self.session.get(url=self.url + '/reverse', headers=self.headers, params=params)
