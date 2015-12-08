#!/usr/bin/env python
# -*-encoding: utf-8

import os
from flask import Flask
app = Flask(__name__)

PATH = os.path.dirname(os.path.abspath(__file__))

DB_NAME = PATH + "/food_base"

path, folder, files = os.walk(PATH).next()

for f in files:
    if f.startswith("__") or f.split(".")[-1] == 'pyc':
        continue
    try:
        package = f.split(".")[0]
        exec("from . import %s" % package)
    except ImportError:
        print package, "ImportError"
        pass
    except SyntaxError:
        print package, "SyntaxError"
        pass