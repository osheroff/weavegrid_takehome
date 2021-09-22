#!/usr/bin/env python

from dirlist import create_app
import sys

if len(sys.argv) < 2:
    sys.exit("usage: app.py [ROOT_PATH]")
app = create_app(sys.argv[1])
app.run()

