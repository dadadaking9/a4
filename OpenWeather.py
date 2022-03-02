# Brandon Chan
# chanbz@uci.edu
# 12383908
from WebAPI import WebAPI

class OpenWeather(WebAPI):
  country_code = None # This class must be initialized. Both Zipcode and Country Code will be set immediately.
  zipcode = None
  #apikey =  None 
  #url = None

  # All of the variables of weather for the validity checker. These are given values in load_data()
  temperature = None
  high_temperature = None
  low_temperature = None
  longitude = None
  latitude = None
  description = None
  humidity = None
  city = None
  sunset = None
  
  def transclude(self, message:str) -> str:
    '''Will insert a description of the weather in place of @weather in the passed in str'''
    if '@weather' in message:
      return message[0:message.index('@weather')] + self.description + message[message.index('@weather') + 8:]

  
  def load_data(self) -> None:
    '''
    Calls the web api using the required values and stores the response in class data attributes.
    '''
    try:
      if self.apikey == None:
        self.apikey = "0fb6a4c23f086c5d7761c423dce4cd69" # default in the case the api key isn't

    # URL is set here given that there's new zipcodes, country codes, and API Keys
      url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.country_code}&appid={self.apikey}"
      local_weather = self._download_url(url)
      
      # Is there a better way to do this?
      self.temperature = local_weather['main']['temp'] # Kelvin
      self.high_temperature = local_weather['main']['temp_max']
      self.low_temperature = local_weather['main']['temp_min']
      self.longitude = local_weather['coord']['lon']
      self.latitude = local_weather['coord']['lat']
      self.description = local_weather['weather'][0]['description']
      self.humidity = local_weather['main']['humidity']
      self.city = local_weather['name']
      self.sunset = local_weather['sys']['sunset']
      print('Data loaded.')

    except: # Handle no internet connection, 404 or 503 connections
      print("Failed to load data. Check your internet connection or if the API key, zip code, or country code have been initialized. Info Below: ")
      print("Initialized API Key: " + self.apikey)
      print('Initialized Country Code: ' + self.country_code)
      print('Initialized Zip Code: ' + self.zipcode)
      print('Initialized URL: ' + f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.country_code}&appid={self.apikey}")
      print("If all information looks properly formatted, either your internet connection is unstable or missing, the API is down, or the API is missing. ")
    

  def __init__(self, zc = '92697', cc = 'US'): #ZC = Zipcode, CC = Country Code, defaults set
    try:
      self.zipcode = zc
      self.country_code = cc
    except:
      print('Error initializaing OpenWeather')


def main() -> None: # OpenWeather shouldn't be ran in here
    pass




if __name__ == '__main__':
    main()