import os
import peewee
from peewee import *

#Must modify this information before production
#Password must be modified.  

#db = MySQLDatabase(os.getenv('DB_NAME', 'Gambler'), user=os.getenv('DB_USER', 'user'), passwd=os.getenv('DB_PW', 'passwd'))
from playhouse.sqlite_ext import SqliteExtDatabase

# PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'configfiles'))
PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))
# db = SqliteDatabase('../configfiles/Gambler.db', pragmas={'journal_mode': 'wal'})
db = SqliteExtDatabase(PROJECT_PATH + '/obs_db.db', regexp_function=True, timeout=3,
                       pragmas={'journal_mode': 'wal'})
class ModelBase(peewee.Model):
	"""Generic model database for Peewee"""
	class Meta:
		database = db
class TournamentOBF(ModelBase)
	"""Databaase model for tournament OBF"""
	tableid = AutoField(null = False)
	event = CharField(null = False)
	sets=CharField(null = False)
	entrants = BlobField(null = False)
	obfversion = CharField(null = False)
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'TournamentOBF'
class EventOBF(ModelBase)
	"""Databaase model for event OBF."""
	tableid = AutoField(null = False)
	name = CharField(null = False)
	eventdate=CharField()
	gameName = CharField()
	tournamentStructure=CharField()
	phase = BlobField()
	originURL = CharField()
	numberEntrants = IntegerField()
	other  BlobField()
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'EventOBF'
class PhaseOBF(ModelBase)
	"""Databaase model for Phase OBF."""
	tableid = AutoField(null = False)
	phaseID = CharField(null = False, unique=True)
	phaseStructure =CharField()
	other = BlobField()
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'PhaseOBF'
class GameOBF(ModelBase)
	"""Databaase model for Phase OBF."""
	tableid = AutoField(null = False)
	gameNumber = IntegerField(null = False, unique=True)
	entrant1Characters =CharField()
	entrant2Characters =CharField()
	stage =CharField()
	entrant1Result =CharField()
	entrant2Result =CharField()
	other = BlobField()
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'GameOBF'
class SetOBF(ModelBase)
	"""Databaase model for Phase OBF."""
	tableid = AutoField(null = False)
	setID = CharField(null = False, unique=True)
	entrant1ID =CharField()
	entrant2ID =CharField()
	status =CharField()
	entrant1Result = CharField()
	entrant2Result = CharField()
	entrant1Result = CharField(null = False)
	entrant2Result = CharField(null = False)
	entrant1Score  = IntegerField(null = False)
	entrant2Score = IntegerField(null = False)
	winnerNextSetID = CharField()
	loserNextSetID  = CharField()
	entrant1PrevSetID = CharField()
	entrant2PrevSetID  = CharField()
	setFormat = CharField()
	phaseID = CharField()	
	roundID = CharField()	
	games = BlobField()
	other = BlobField()
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'SetOBF'
class PersonalInformationOBF(ModelBase)
	"""Databaase model for Phase OBF."""
	tableid = AutoField(null = False)
	name = CharField()
	country =CharField()
	gender =CharField()
	pronouns =CharField()
	language = BlobField()
	other = BlobField()
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'PersonalInformationOBF'
class EntrantOBF(ModelBase)
	"""Databaase model for Phase OBF."""
	tableid = AutoField(null = False)
	setid = CharField(null = False, unique=True)
	entrantTeam =BooleanField()
	entrantTag =CharField()
	initialSeed =IntegerField()
	finalPlacement =IntegerField()
	personalInformation =BlobField()
	other = BlobField()
	class Meta:
		database =db
		#table_name is table for the data.
		table_name = 'EntrantOBF'