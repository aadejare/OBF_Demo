# Script to communicate OBS to SQLITE database

import os
import peewee
from peewee import *

#Must modify this information before production
#Password must be modified.  

from playhouse.sqlite_ext import SqliteExtDatabase

# PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'configfiles'))
PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))
db = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
                       pragmas={'journal_mode': 'wal'})
class ModelBase(peewee.Model):
	"""Generic model database for Peewee"""
	class Meta:
		database = db

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
	class Meta:
		database = db

class EntrantObf(BaseModel):
	entrantTag = TextField(column_name='entrantTag', null=True)
	entrantTeam = BooleanField(column_name='entrantTeam', null=True)
	finalPlacement = IntegerField(column_name='finalPlacement', null=True)
	initialSeed = IntegerField(column_name='initialSeed', null=True)
	other = BlobField(null=True)
	personalInformation = BlobField(column_name='personalInformation', null=True)
	setID = TextField(column_name='setID', unique=True)
	tableid = TextField(unique=True, primary_key=True)
    
	class Meta:
		database =db
		table_name = 'EntrantOBF'

class CharactersObf(BaseModel):
	entrantCharacterName = TextField(column_name='entrantCharacterName', unique=True)
	entrantCharacterNameID = TextField(column_name='entrantCharacterNameID')
	tableid = AutoField()
	class Meta:
		database =db
		table_name = 'CharactersObf'

class EventObf(BaseModel):
	eventDate = TextField(null=True)
	gameName = TextField(column_name='gameName', null=True)
	name = TextField()
	numberEntrants = IntegerField(column_name='numberEntrants', null=True)
	originURL = TextField(column_name='originURL', null=True)
	other = BlobField(null=True)
	phaseID = TextField(column_name='phaseID', null=True, unique=True)
	phases = BlobField(null=True)
	ruleset = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)
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
	tableid = TextField(unique=True, primary_key=True)

	class Meta:
		database =db
		table_name = 'GameOBF'

class PersonalInformationObf(BaseModel):
	country = TextField(null=True)
	gender = TextField(null=True)
	language = BlobField(null=True)
	name = TextField(null=True)
	other = BlobField(null=True)
	pronouns = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)
	entrant_tag =  TextField(column_name='entrant_tag',null=False)

	class Meta:
		database =db
		table_name = 'PersonalInformationOBF'

class PhaseObf(BaseModel):
	other = BlobField(null=True)
	phaseID = TextField(column_name='phaseID', unique=True)
	phaseStructure = TextField(column_name='phaseStructure', null=True)
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
	loserNextSetID = TextField(column_name='loserNextSetID', null=True)
	other = BlobField(null=True)
	phaseId = TextField(column_name='phaseID', null=True)
	roundId = TextField(column_name='roundID', null=True)
	setFormat = TextField(column_name='setFormat', null=True)
	setID = TextField(column_name='setID', unique=True)
	status = TextField(null=True)
	tableid = TextField(unique=True, primary_key=True)
	winnernextsetID = TextField(column_name='winnerNextSetID', null=True)

	class Meta:
		database =db
		table_name = 'SetOBF'

class TournamentObf(BaseModel):
	entrants = BlobField()
	event = TextField()
	obfversion = TextField(null=True,
	constraints=[Check("obfversion\\ in\\ \\('v0\\.1',\\ 'v0\\.2'\\)")])
	sets = BlobField()
	tableid = TextField(unique=True, primary_key=True)
	
	class Meta:
		database =db
		table_name = 'TournamentOBF'

