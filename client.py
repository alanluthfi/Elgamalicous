import socket
from PIL import Image
#import random
#from math import pow
#import versi1
import RSA
#import numpy as np
#import pickle
import random
from math import pow

a=random.randint(2,10)

#To fing gcd of two numbers
def gcd(a,b):
    if a<b:
        return gcd(b,a)
    elif a%b==0:
        return b
    else:
        return gcd(b,a%b)

#For key generation i.e. large random number
def gen_key(q):
    key= random.randint(pow(10,20),q)
    while gcd(q,key)!=1:
        key=random.randint(pow(10,20),q)
    return key

def power(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c;
        y=(y*y)%c
        b=int(b/2)
    return x%c

#For asymetric encryption
def encryption(msg,q,h,g):
    ct=[]
    k=gen_key(q)
    s=power(h,k,q)
    p=power(g,k,q)
    for i in range(0,len(msg)):
        ct.append(msg[i])
    #print("g^k used= ",p)
    #print("g^ak used= ",s)
    for i in range(0,len(ct)):
        ct[i]=s*ord(ct[i])
    return ct,p


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('localhost', 1002))  # 127.0.0.1

# option = input("Send Image/Text? ")
option = "text"
client.send(option.encode("ascii"))

if option.lower() == "image":
    imagename = input("Input image name: ")
    # image encryption
    image = Image.open(imagename)
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    string_pixels_test = []
    for row in pixels:
        for tup in row:
            string_pixels_test.append(RSA.enc(tup))
    
    string_pixels_test.append(str(image.size[0]).zfill(5))
    string_pixels_test.append(str(image.size[1]).zfill(5))
    string_pixels_test = "".join(string_pixels_test)
    client.send(string_pixels_test.encode('ascii'))
    image.close()

elif option.lower() == "text":
    msg = input("message: ")
    q=random.randint(pow(10,20),pow(10,50))
    g=random.randint(2,q)
    key=gen_key(q)
    h=power(g,key,q)
    ct,p=encryption(msg,q,h,g)

    print("CT blom di encode= ",ct)
    print(type(ct))
    print("P blom di encode = ",p)
    print(type(p))

    ct = str(ct)
    ct = ct.encode("ascii")

    p = str(p)
    p = p.encode("ascii")

    key = str(key)
    key = key.encode("ascii")

    q = str(q)
    q = q.encode("ascii")


    print("CT = ",ct)
    print(type(ct))
    print("P = ",p)
    print(type(p))
    print("key = ",key)
    print(type(key))
    print("Q = ",q)
    print(type(q))

    client.send(ct)
    client.send(p)
    client.send(key)
    client.send(q)
    #client.send(encrypted.encode("ascii"))
    print("Message sent.")

else:
    print("Input error!")

client.close()