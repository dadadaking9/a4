# Brandon Chan
# chanbz@uci.edu
# 12383908

from abc import ABC, abstractmethod
import urllib, json  
from urllib import request,error

class WebAPI(ABC):
  # Web API Common Variables:
  apikey = None
  url = None

  def _download_url(self, url: str) -> dict: # Heavily inspired by sample code
    '''Downloads API information from the passed url.'''
    response = None
    r_obj = None

    try:
      response = urllib.request.urlopen(url) # Open the URL to access the information inside
      json_results = response.read() # Save the information accessed
      r_obj = json.loads(json_results) # Load the information into a dictionary-- something we can work with
    except urllib.error.HTTPError as e: # Taken from sample _download_url() for error handeling 
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
    finally:
      if response != None:
        response.close() # Must close open urls

    return r_obj # Return the dictionary of information opened from the URL
	
  def set_apikey(self, apikey:str) -> None:
    '''Given an API key, set it to this particualr web api'''
    try:
      self.apikey = apikey
      print('API Key Set as following: ' + self.apikey)
    except:
      print('Setting API Key to variable failed.')
	
  @abstractmethod
  def load_data(self):
    pass
	
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass
