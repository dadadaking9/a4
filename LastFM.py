# Brandon Chan
# chanbz@uci.edu
# 12383908
from WebAPI import WebAPI

class LastFM(WebAPI):
    # Variables
    artists = []
    song_names = []
    number_of_songs = 10

    # apikey = None (from WebAPI)
    # url = None (from WebAPI)

    # _download_url(self, url: str) -> dict

    # set_apikey(self, apikey:str)

    def load_data(self):
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={self.apikey}&format=json"
        data = self._download_url(url)

        # 0 Specifies the first song
        for n in range(self.number_of_songs):
            self.artists.append(data['tracks']['track'][n]['artist']['name'])
            self.song_names.append(data['tracks']['track'][n]['name'])
        

    def transclude(self, message:str) -> str:
        '''Will insert the current top artist in @lastfm'''
        if '@lastfm' in message:
            return message[0:message.index('@lastfm')] + self.artists[0] + message[message.index('@lastfm') + 7:]
    

    def __init__(self):
        # Default Key in case none is set. 
        self.apikey = 'fe4159cc32118e7a29cd128c1eb0e4d9'