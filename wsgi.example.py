# coding: utf-8

import sys
import os

# SET THIS!
# this path points to a folder that contains the settings folder and the
# tagarela package folder
this_path = "/path/to/folder"

# SET THIS!
# this path points to the virtual env
activate_this = "/path/to/virtualenv/bin/activate_this.py"

sys.path.insert(0, this_path)
execfile(activate_this, dict(__file__=activate_this))
os.chdir(this_path)

# give wsgi the "application"
from esiclivre.app import app as application
# application = app()
