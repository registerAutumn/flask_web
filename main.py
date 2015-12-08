#!/usr/bin/env python
# -*- encoding: utf-8
import sys
import os

try:
    exec("from %s import *" % sys.argv[1])
    app.config['SECRET_KEY'] = os.urandom(10)
    app.config['DEBUG'] = True
    app.run(host="127.0.0.1", port=int(sys.argv[2]), debug=True)
except ImportError:
    print "error"