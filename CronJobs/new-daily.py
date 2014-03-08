# import imp
# search = imp.load_source('search', 'C:\Users\Roshan Bhandari\Desktop\project repos\foodtrade\mainapp\classes\Search.py')
from import_file import import_file
import os
APP_ROOT = os.path.realpath('.')
APP_ROOT = APP_ROOT.replace('CronJobs','')
MONGO_PATH = APP_ROOT.replace('\\','/') + '/foodtrade/mainapp/classes/MongoConnection.py'
print MONGO_PATH
mylib = import_file(MONGO_PATH)
mylib = import_file('/foodtrade/mainapp/classes/Search.py')
