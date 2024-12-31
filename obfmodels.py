# Script to communicate OBS to SQLITE database

import os
import peewee
from peewee import *

#Must modify this information before production
#Password must be modified.  

from playhouse.sqlite_ext import SqliteExtDatabase

# PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'configfiles'))
# make db proxy 
# Link https://docs.peewee-orm.com/en/latest/peewee/database.html#deferring-initialization
# db =  DatabaseProxy()  
# PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))
# db = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
#                        pragmas={'journal_mode': 'wal'})
#
db = DatabaseProxy()

class ModelBase(peewee.Model):
	"""Generic model database for Peewee"""
	class Meta:
		database = db

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
	class Meta:
		database = db

class CharactersObf(BaseModel):
	entrantCharacterName = TextField(column_name='entrantCharacterName', unique=True)
	entrantCharacterNameID = TextField(column_name='entrantCharacterNameID')
	tableid = AutoField()
	class Meta:
		database =db
		table_name = 'CharactersObf'

class EntrantObf(BaseModel):
	entrantID = TextField(column_name='entrantID', null=False)
	entrantTag = TextField(column_name='entrantTag')
	entrantTeam = TextField(column_name='entrantTeam', null=True)
	finalPlacement = IntegerField(column_name='finalPlacement', null=True)
	initialSeed = IntegerField(column_name='initialSeed', null=True)
	other = BlobField(null=True)
	tableid = TextField(unique=True, primary_key=True)
	tournamentID = TextField()

    
	class Meta:
		database =db
		table_name = 'EntrantOBF'

class EventObf(BaseModel):
	eventDate = TextField(null=True)
	gameName = TextField(column_name='gameName', null=True)
	name = TextField()
	numberEntrants = IntegerField(column_name='numberEntrants', null=True)
	originURL = TextField(column_name='originURL', null=True)
	other = BlobField(null=True)
	ruleset = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)
	tournamentID = TextField()
	tournamentStructure = TextField(column_name='tournamentStructure', null=True)

	class Meta:
		database =db
		table_name = 'EventOBF'

class GameObf(BaseModel):
	entrant1Characters = BlobField(column_name='entrant1Characters', null=True)
	entrant1Result = TextField(column_name='entrant1Result', null=True,constraints=[Check("entrant1Result in ('win','lose','draw','Win','Lose','Draw','WIN','LOSE','DRAW')")])
	entrant2Characters = BlobField(column_name='entrant2Characters', null=True)
	entrant2Result = TextField(column_name='entrant2Result', null=True,constraints=[Check("entrant2Result in ('win','lose','draw','Win','Lose','Draw','WIN','LOSE','DRAW')")])
	gameNumber = IntegerField(column_name='gameNumber', unique=True)
	other = BlobField(null=True)
	stage = TextField(null=True)
	setID = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)

	class Meta:
		database =db
		table_name = 'GameOBF'

class PersonalInformationObf(BaseModel):
	country = TextField(null=True)
	gender = TextField(null=True)
	entrant_language = BlobField(null=True)
	name = TextField(null=True)
	other = BlobField(null=True)
	pronouns = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)
	entrantTag =  TextField(column_name='entrantTag',null=False)
	entrant_prefix = TextField(null=True)

	class Meta:
		database =db
		table_name = 'PersonalInformationOBF'

class PhaseObf(BaseModel):
	other = BlobField(null=True)
	phaseID = TextField(column_name='phaseID', unique=True)
	phaseStructure = TextField(column_name='phaseStructure', null=True)
	name = TextField(column_name='name', null=True)
	eventID = TextField(column_name='eventID', null=True)
	tableid = TextField(unique=True, primary_key=True)

	class Meta:
		database =db
		table_name = 'PhaseOBF'

class SetObf(BaseModel):
	entrant1ID = TextField(column_name='entrant1ID', null=True)
	entrant1PrevSetID = TextField(column_name='entrant1PrevSetID', null=True)
	entrant1Result = TextField(column_name='entrant1Result', null=True)
	entrant1Score = IntegerField(column_name='entrant1Score')
	entrant2ID = TextField(column_name='entrant2ID', null=True)
	entrant2PrevSetID = TextField(column_name='entrant2PrevSetID', null=True)
	entrant2Result = TextField(column_name='entrant2Result', null=True)
	entrant2Score = IntegerField(column_name='entrant2Score')
	games = BlobField(null=True)
	entrant1NextSetID = TextField(column_name='entrant1NextSetID', null=True)
	other = BlobField(null=True)
	phaseID = TextField(column_name='phaseID', null=True)
	roundID = TextField(column_name='roundID', null=True)
	setFormat = TextField(column_name='setFormat', null=True)
	setID = TextField(column_name='setID')
	status = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)
	entrant2NextSetID = TextField(column_name='entrant2NextSetID', null=True)
	tournamentID = TextField(column_name='tournamentID')

	class Meta:
		database =db
		table_name = 'SetOBF'

class TournamentObf(BaseModel):
	tournamentTitle = TextField(column_name='tournamentTitle')
	SetGameResult = TextField()
	description = TextField()
	obfversion = TextField(null=True,
	constraints=[Check("obfversion\\ in\\ \\('v0\\.1',\\ 'v0\\.2'\\)")])
	tournamentID = TextField(column_name='tournamentID',unique=True)
	tableid = TextField(unique=True, primary_key=True)
	
	class Meta:
		database =db
		table_name = 'TournamentOBF'

