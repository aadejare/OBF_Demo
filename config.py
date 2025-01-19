# config.py
# Config file to import varibales
import os
import peewee
#Must modify this information before production
#Password must be modified.  

# Link https://docs.peewee-orm.com/en/latest/peewee/database.html#deferring-initialization

db = peewee.Proxy()
PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))
