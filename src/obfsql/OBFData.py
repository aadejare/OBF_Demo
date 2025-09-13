#!/usr/bin/env python
"""
OBFData.py
Atomically call differnet parts of the OBF Data within the database

"""
import re, os, sys, time, shutil, json

PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))

from playhouse.sqlite_ext import SqliteExtDatabase
sys.path.insert(1,PROJECT_PATH)
from obfmodels import db as obfdb
import Event, MatchSet, Entrant, Game, Phase, Tournament, PersonalInformation

class OBFData_Event(Event.Event):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			self.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass

class OBFData_Game(Game.Game):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			self.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass

class OBFData_Phase(Phase.Phase):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			self.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass


class OBFData_MatchSet(MatchSet.MatchSet):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			self.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass

class OBFData_Tournament(Tournament.Tournament):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			self.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass


class OBFData_Entrant(Entrant.Entrant):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			cself.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass

class OBFData_PersonalInformation(PersonalInformation.PersonalInformation):
	def __init__(self):
		self.db = obfdb
		super().__init__(self)

			
	def connect(self,dbtype = None, path=None, database=None, **kwargs):
		"""
		Connect the object to a database to access the bracket information
		dbtype :str: Type of database to use
		path :str: Path to the database (either url or directory path)
		database :str: Database name
				
		"""
# 		self.db.initialize_proxy(dbtype,path,database,**kwargs)
		if type(dbtype)!= str:
			return None
		if dbtype.lower() in ['sqlite', 'sqlite3','lite','default']:
# 			db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
# 							   pragmas={'journal_mode': 'wal'})
			self.db.initialize(SqliteExtDatabase(path + database, regexp_function=True, timeout=3,
							   pragmas={'journal_mode': 'wal'}))
# 			self.db = config.db
		if dbtype.lower() in ['postgres', 'post','postgresql']:
			cself.db.initialize(PostgresqlDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw'],
                        port=kwargs['port']))
# 			self.db = config.db
		if dbtype.lower()  in ['mariadb', 'mysql','mysqldb']:
			self.db.initialize(MySQLDatabase(database, user=kwargs['user'], 
						host=kwargs['host'],
                        password=kwargs['pw']))
# 			self.db = config.db
		else:
			pass
