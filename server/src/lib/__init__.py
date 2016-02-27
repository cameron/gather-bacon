import time

def profile(name):
  start = time.time()
  def done():
    print (time.time() - start), name
