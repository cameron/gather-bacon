import sys

from flask import Flask, got_request_exception
from lib import resources

app = Flask(__name__)
app.secret_key = 'righteous rabbit electrode pike'

resources.setup_dbpool()

def debug(sender, exception, **kw):
  import sys
  import pdb
  import traceback
  traceback.print_exc()
  pdb.post_mortem(sys.exc_info()[2])

#got_request_exception.connect(debug, app)

import sys

def info(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
    # we are in interactive mode or we don't have a tty-like
    # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception
        traceback.print_exception(type, value, tb)
        print
        # then start the debugger in post-mortem mode.
        # pdb.pm() # deprecated
        pdb.post_mortem(tb) # more modern

#sys.excepthook = info

