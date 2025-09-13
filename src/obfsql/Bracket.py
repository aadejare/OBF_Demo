#!/usr/bin/env python
"""
Bracket.py
Retrieve all the data in the proper format.
"""
import re, os, sys, time, shutil, json

PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))

from playhouse.sqlite_ext import SqliteExtDatabase
sys.path.insert(1,PROJECT_PATH)
from obfmodels import db as obfdb
import Event, MatchSet, Entrant, Game, Phase, Tournament





class Bracket():
	def __init__(self):
		self.db = obfdb
			
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

	def retrieve(self, tournamentID=None, tournamentTitle=None, eventName=None):
		"""
		Retrive the Tournament from the SQL Database and returns object
		tournamentID :str: required, tournament ID to locate the tournament
		tournamentTitle :str: optional, tournament title. Note, will select latest tournament with same title
		eventName :str: name of the event to retrieve  Note, will select latest event with same title
		"""
		if tournamentID is None and tournamentTitle is None:
			print("No tournament retrieval paramter was entered")
			return None
		elif tournamentID is None and tournamentTitle is not None:
			print("Warning: Title retrival will retrieve the latest tournament entered with the title")
			tourn_ex = Tournament.Tournament(tournamentTitle=tournamentTitle)
			tourn_ex.gettournamentID()
		else:
			tourn_ex = Tournament.Tournament(tournamentID=tournamentID)
		OBF = tourn_ex.exporttournament()
		# Get event data
		event_ex = Event.Event(name=eventName, tournamentID=tourn_ex.tournamentID)
		event_ex2 = event_ex.exportevent()
		del event_ex2['tournamentID']
		OBF['event'] = event_ex2
		phase_data = Phase.Phase(name=event_ex.name)
		OBF['phases'] = phase_data.exportphases()
		set_ex = MatchSet.MatchSet(
					tournamentID=tourn_ex.tournamentID)
		set_ex2 = set_ex.exportsets()
		for i in range(0,len(set_ex2)):
			game_ex=Game.Game(setID=set_ex2[i]['setID'])
			set_ex2[i]['games'] = game_ex.exportgames()
		OBF['sets'] = [set_ex2]
		entrant_ex = Entrant.Entrant(tournamentID = tourn_ex.tournamentID )
		OBF['entrants'] = entrant_ex.exportentrants()
		OBF['event'] = event_ex2
		return OBF
	def retrievejson(self, tournamentID=None, tournamentTitle=None, eventName=None):
		"""
		Retrive the Tournament from the SQL Database and returns JSON
		tournamentID :str: required, tournament ID to locate the tournament
		tournamentTitle :str: optional, tournament title. Note, will select latest tournament with same title
		eventName :str: name of the event to retrieve  Note, will select latest event with same title
		"""
		OBF= retrieve(tournamentID, tournamentTitle, eventName)
		return json.dumps(OBF, indent=4)
# 
	def store(self, bracket=None):
		if bracket is None:
			return None
		if type(bracket) == str:
			bracket = json.loads(bracket)
		if 'tournamentID' not in bracket:
			print("Not here")
			return None
		tourn_bracket = Tournament.Tournament(tournamentTitle=bracket['description'],\
			tournamentID=bracket['tournamentID'], obfversion=bracket['version'],\
			description=bracket['description'], SetGameResult=bracket['SetGameResult'])
		tourn_bracket.savetournament('new')
		event_list = None
		if not isinstance(bracket['event'], list):
			event_list = [bracket['event']]
		else:
			event_list = bracket['event']
		for eventx in event_list :
# 			print(eventx)
			event_obf = eventx
			event_bracket = Event.Event(eventDate=event_obf['eventDate'], gameName=event_obf['gameName'],\
						ruleset=event_obf['ruleset'],originURL=event_obf['originURL'],\
						name=event_obf['name'], numberEntrants = event_obf['numberEntrants'],
						tournamentStructure= event_obf['tournamentStructure'],
						tournamentID= tourn_bracket.tournamentID,)
			event_bracket.saveevent('new')
# 			print ('Next Phase Data: \n\n')
		for ix in bracket['phases']:
			phase_bracket = Phase.Phase( phaseID= ix['phaseID'],
									phaseStructure=ix['phaseStructure'],
									name=event_bracket.name)
			phase_bracket.savephase(savedata='new')	
		for i in range(0, len(bracket['sets'])):
			set_bracket_parse = bracket['sets'][i]
			set_bracket = MatchSet.MatchSet(entrant1ID=set_bracket_parse['entrant1ID'],\
					entrant2ID=set_bracket_parse['entrant2ID'], status=set_bracket_parse['status'], \
					entrant1Result=set_bracket_parse['entrant1Result'], \
					entrant2Result=set_bracket_parse['entrant2Result'],\
					entrant1Score=set_bracket_parse['entrant1Score'], \
					entrant2Score=set_bracket_parse['entrant2Score'],\
					entrant1NextSetID=set_bracket_parse['entrant1NextSetID'], \
					entrant2NextSetID=set_bracket_parse['entrant2NextSetID'],\
					setFormat=set_bracket_parse['setFormat'], \
					phaseID=phase_bracket.phaseID,
					setID =set_bracket_parse['setID'],
					tournamentID=tourn_bracket.tournamentID)
# 			print(set_bracket_parse['setID'])
			set_bracket.saveset('new')
# 			print("THIS IS SET ID: " + str(set_bracket.setID))
			game_bracket_set = set_bracket_parse['games']
# 			print ('Game bracket: \n\n\n')
			for jx in game_bracket_set:
				game_bracket_parse = jx
				game_bracket = Game.Game(gameNumber=game_bracket_parse['gameNumber'], 
				entrant1Characters=game_bracket_parse['entrant1Characters'],\
				entrant2Characters=game_bracket_parse['entrant2Characters'],\
					stage=game_bracket_parse['stage'], \
					entrant1Result=game_bracket_parse['entrant1Result'],\
					 entrant2Result=game_bracket_parse['entrant2Result'],\
					 setID=set_bracket.setID,\
						other=None)
				game_bracket.savegame('new')
# 				print(set_bracket.exportset())
# 		print ('Entrant bracket: \n\n\n')
# 		print(bracket['entrants'])
		for i in range(0, len(bracket['entrants'])):
			entrant_parse = bracket['entrants'][i]
# 			print (entrant_parse['entrantTag'],)
			entrant_Data = Entrant.Entrant(entrantID = entrant_parse['entrantTag'], 
									entrantTag = entrant_parse['entrantTag'], 
							finalPlacement=entrant_parse['finalPlacement'], 
							initialSeed=entrant_parse['initialSeed'], 
							personalInformation =entrant_parse['personalInformation'],
							tournamentID = tourn_bracket.tournamentID )
# 			print(entrant_Data.entrantTag)
			entrant_Data.saveentrant('update')
# 			print(entrant_Data.exportentrants())
		return 0