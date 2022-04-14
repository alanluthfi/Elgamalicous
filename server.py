import socket
from PIL import Image
import RSA
import versi1
import random
from math import pow

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('localhost', 1002))  # 127.0.0.1
server.listen()

client_socket, client_address = server.accept()

option = client_socket.recv(2048).decode('ascii')
if option.lower() == "image":
    print("Receiving encrypted image...")
    encrypted_string = client_socket.recv(16384000).decode('ascii')
    
    imagename = input("Decrypting image...\nInput image name: ")
    pixels_test = RSA.dec(encrypted_string[:-10])
    # print(pixels_test)
    image_test = Image.new('RGBA',(int(encrypted_string[-10:-5]), int(encrypted_string[-5:])))
    image_test.putdata(pixels_test)
    image_test.save('{}.png'.format(imagename))
    
    print("Image Received.")

elif option.lower() == "text":
    print("Receiving text...")
    message = client_socket.recv(2048).decode('ascii')
    message2 = client_socket.recv(2048).decode('ascii')
    message3 = client_socket.recv(2048).decode('ascii')
    message4 = client_socket.recv(2048).decode('ascii')
    print("encrypted message: ", end="")
    print(message)
    print(type(message))
    print("encrypted p: ", end="")
    print(message2)
    ct = message
    ct = ct.split()
    print("ct split: ", end="")
    print(ct)
    print(type(ct))
    p = message2
    p = int(message2)
    print("p int: ", end="")
    print(p)
    print(type(p))

    key = message3
    key = int(message3)
    print("key: ", end="")
    print(key)
    print(type(key))

    q = message4
    q = int(message4)
    print("q: ", end="")
    print(q)
    print(type(q))

    # q=random.randint(pow(10,20),pow(10,50))
    # key=versi1.gen_key(q)
    pt=versi1.decryption(ct,p,key,q)
    d_msg=''.join(pt)
    print("decrypted message: ", end="")
    print(d_msg)

client_socket.close()