#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/interbrew/")
from interbrew import app as application
#application.secret_key = 'help'
