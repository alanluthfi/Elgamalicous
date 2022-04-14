from email import message
import socket
import threading
from random import randrange as rr

import Elgamal

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.8.131.34'
client.connect((host, 55555))
x = 2157
y_target = 1398
def receive():
  while True:
    try:
      # Receive Message From Server
      # If 'NICK' Send Nickname
      message = client.recv(4096).decode('ascii')
      if message == 'NICK':
        client.send(nickname.encode('ascii'))
      else:
        try:
          a, b = message.split("$ELG$A$MAL$")[1:]
          m = Elgamal.dec(a, b, x)
          # print("Ciphertext (a, b) = ({}, {})".format(a, b))
          print("{}: {}".format(nickname, m))
        except:
          print("{}".format(message))
          
    except:
      # Close Connection When Error
      print("An error occured!")
      client.close()
      break

# Sending Messages To Server
def write():
  while True:
    input_message = input()
    a, b = Elgamal.enc(y_target, input_message)
    # message = '{}: {}'.format(nickname, input_message)
    message = "{}$ELG$A$MAL${}$ELG$A$MAL${}".format(nickname, a, b)
    client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()