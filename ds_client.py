# Brandon CHan
# chanbz@uci.edu
# 12383908
import socket
import json
import ds_protocol
def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  HOST = '168.235.86.101'
  PORT = 3021
  
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client: # client is using ipv4 and is TCP [sockstream]
    client.connect((HOST, PORT)) # Connect to the server

    send = client.makefile('w') # Write the info
    recv = client.makefile('r') # Read the info

    print("client connected to {HOST} on {PORT}")
    send.write(ds_protocol.join(username, password) + '\r\n')
    send.flush()
    srv_msg = recv.readline()
    server_response = json.loads(srv_msg)
    token = server_response['response']['token']
    print("Response:", srv_msg) #DELETE | This tells us the server's response

    #print('message type:', type(message))
    #the_message = json.loads(message)
    #the_message = the_message["post"]['entry']
    #the_message = message.get_entry()
    #print('the_message:', the_message)
    

    send.write(ds_protocol.post(token, message) + '\r\n') # This might break if that post doesn't exist. How can we avoid that?
    send.flush()
    srv_msg = recv.readline()
    server_response = json.loads(srv_msg)
    print(server_response)

    send.write(ds_protocol.bio(token, bio) + '\r\n')
    send.flush()
    srv_msg = recv.readline()
    server_response = json.loads(srv_msg)
    print(server_response)

    

