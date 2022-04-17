import socket
import threading
from random import randrange as rr

from Elgamal import p, public_key, enc, dec


# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.8.131.5'
client.connect((host, 55555))

x = rr(2, p - 1)
pub_key = 0

def receive():
  global pub_key
  while True:
    try:
      # Receive Message From Server
      # If 'NICK' Send Nickname
      message = client.recv(1024).decode('ascii')
      if message == 'NICK':
        client.send(nickname.encode('ascii'))
      else:
        try:
          pub_key = int(message)
          message = 'public key received: {}'.format(pub_key)
          print(message)
        except:
          try:
            nick, a, b = message.split(": ")
            decrypted = dec(a, b, x)
            print('{}: {}'.format(nick, decrypted))
          except:
            print(message)
            # pass
    except:
      # Close Connection When Error
      print("An error occured!")
      client.close()
      break

# Sending Messages To Server
def write():
  first = True
  while True:
    if first:
      input("sending pub key. Press enter...\n")
      message = '{}'.format(public_key(x))
      first = False
    else:
      input_message = input('')
      encrypted = enc(pub_key, input_message)
      message = '{}: {}: {}'.format(nickname, *encrypted)
    client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

