import time

def profile(name):
  start = time.time()
  def done():
    print (time.time() - start), name
  return done

# TODO use bcrypt
from md5 import md5
def gen_token(v):
  return str(md5(v).hexdigest())
