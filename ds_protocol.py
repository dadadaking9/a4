# Brandon CHan
# chanbz@uci.edu
# 12383908

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['foo','baz'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)

def bio(token: str, biography: dict):
  '''Returns the data neccessary to post a bio to the website given the token'''
  data = {"token":token, "bio": biography}
  return json.dumps(data)
  

def post(token: str, message):
  '''Returns the data neccessary to post a message to the website given the user token and the message that is wished to be posted (given from a dsu profile file)'''
  data = {"token":token, "post": message}
  return json.dumps(data)


def join(username: str, password: str):
  '''Returns the JSON data neccessary to join the website given a username and password'''
  data = {"join": {"username": username,"password": password,"token":""}}
  return json.dumps(data)
  
