#!/usr/bin/env python
# -*-encoding: utf-8

import os
from flask import Flask
app = Flask(__name__)

path, folder, files = os.walk("./class_/").next()

for f in files:
    if f.startswith("__") or f.split(".")[-1] == 'pyc':
        continue
    try:
        package = f.split(".")[0]
        exec("from . import %s" % package)
    except ImportError:
        print "%s Import Error" % package
    except SyntaxError:
        pass