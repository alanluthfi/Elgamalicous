from random import randrange as rr

# p dan g disepakati (static)
p = 2273  # bilangan prima (public)

# g merupakan akar primitif dari p (public)
g = 0
for _ in range(1, p):
  g1 = [_**i % p for i in range(1, p)]
  g2 = [_**i % p for i in range(p, 2*p-1)]
  if g1 == g2 and len(set(g1)) == p-1:
    g = _
    break

def public_key(x):
  # x = 243  # bilangan bulat acak (private key)
  y = g**x % p  # dikirimkan ke client lawan (public key -> y, g, p)
  return y

def enc(y, m):

  """1. memilih bilangan bulat k acak 
     2. menghitung a = g**k % p
     3. menghitung b = y**k * m % p ||| y dari public key

  """
  ord_plain = [ord(c) for c in m]
  a = []
  b = []
  for m in ord_plain:
    k = rr(1, p-1) # 1463
    a.append(str(g**k % p).zfill(4))
    b.append(str((y**k * m) % p).zfill(4)) # 461
  a = "".join(a)
  b = "".join(b)
  return a, b

def dec(a, b, x):

  """1. ai = a**(p-1-x) % p
     2. m = b * ai % p
  """
  int_a = [int(a[i:i+4]) for i in range(0, len(a), 4)]
  int_b = [int(b[i:i+4]) for i in range(0, len(b), 4)]
  m = []
  for i in range(len(int_a)):
    ai = int_a[i]**(p-1-x) % p
    m.append(int_b[i] * ai % p)

  return "".join([chr(i) for i in m])

# x = 243  # bilangan bulat acak (private key)
# y = g**x % p  # dikirimkan ke client lawan (public key -> y, g, p)

# K = y**x % p  # client 1 menghitung nilai K

# X = g**x % p  # dikirimkan ke client 2 (public key -> X, g, p)
# y = 158  # bilangan bulat acak (private key)
# K_hat = X**y % p  # client 1 menghitung nilai K_hat