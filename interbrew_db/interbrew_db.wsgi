#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/interbrew_db/")
from interbrew_db import app as application
#application.secret_key = 'help'
