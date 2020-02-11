import sys
import logging
logging.basicConfig(stream=sys.stderr)
# For carbon
sys.path.insert(0,"/var/www/studiosleepygiraffe/studiosleepygiraffe")

# For everyone else
sys.path.insert(0,'/home/toben/Code/ssg/studiosleepygiraffe/studiosleepygiraffe')

from studiosleepygiraffe import app as application
application.secret_key = 'Add your secret key'
