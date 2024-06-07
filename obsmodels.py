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
	entrant_tag = TextField(column_name='entrantTag', null=True)
	entrant_team = BooleanField(column_name='entrantTeam', null=True)
	final_placement = IntegerField(column_name='finalPlacement', null=True)
	initial_seed = IntegerField(column_name='initialSeed', null=True)
	other = BlobField(null=True)
	personal_information = IntegerField(column_name='personalInformation', null=True)
	set_id = TextField(column_name='setID', unique=True)
	tableid = AutoField(null=True)
    
	class Meta:
		database =db
		table_name = 'EntrantOBF'

class EventObf(BaseModel):
	eventdate = TextField(null=True)
	game_name = TextField(column_name='gameName', null=True)
	name = TextField()
	number_entrants = IntegerField(column_name='numberEntrants', null=True)
	origin_url = TextField(column_name='originURL', null=True)
	other = BlobField(null=True)
	phase_id = TextField(column_name='phaseID', null=True, unique=True)
	phases = BlobField(null=True)
	ruleset = TextField(null=True)
	tableid = AutoField(null=True)
	tournament_structure = TextField(column_name='tournamentStructure', null=True)

	class Meta:
		database =db
		table_name = 'EventOBF'

class GameObf(BaseModel):
	entrant1_characters = TextField(column_name='entrant1Characters', null=True)
	entrant1_result = TextField(column_name='entrant1Result', null=True)
	entrant2_characters = TextField(column_name='entrant2Characters', null=True)
	entrant2_result = TextField(column_name='entrant2Result', null=True)
	game_number = IntegerField(column_name='gameNumber', unique=True)
	other = BlobField(null=True)
	stage = TextField(null=True)
	tableid = AutoField(null=True)

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
	tableid = AutoField(null=True)

	class Meta:
		database =db
		table_name = 'PersonalInformationOBF'

class PhaseObf(BaseModel):
	other = BlobField(null=True)
	phase_id = TextField(column_name='phaseID', unique=True)
	phase_structure = TextField(column_name='phaseStructure', null=True)
	tableid = AutoField(null=True)

	class Meta:
		database =db
		table_name = 'PhaseOBF'

class SetObf(BaseModel):
	entrant1_id = TextField(column_name='entrant1ID', null=True)
	entrant1_prev_set_id = TextField(column_name='entrant1PrevSetID', null=True)
	entrant1_result = TextField(column_name='entrant1Result', null=True)
	entrant1_score = IntegerField(column_name='entrant1Score')
	entrant2_id = TextField(column_name='entrant2ID', null=True)
	entrant2_prev_set_id = TextField(column_name='entrant2PrevSetID', null=True)
	entrant2_result = TextField(column_name='entrant2Result', null=True)
	entrant2_score = IntegerField(column_name='entrant2Score')
	games = BlobField(null=True)
	loser_next_set_id = TextField(column_name='loserNextSetID', null=True)
	other = BlobField(null=True)
	phase_id = TextField(column_name='phaseID', null=True)
	round_id = TextField(column_name='roundID', null=True)
	set_format = TextField(column_name='setFormat', null=True)
	set_id = TextField(column_name='setID', unique=True)
	status = TextField(null=True)
	tableid = AutoField(null=True)
	winner_next_set_id = TextField(column_name='winnerNextSetID', null=True)

	class Meta:
		database =db
		table_name = 'SetOBF'

class TournamentObf(BaseModel):
	entrants = BlobField()
	event = TextField()
	obfversion = TextField(null=True)
	sets = BlobField()
	tableid = AutoField(null=True)
	
	class Meta:
		database =db
		table_name = 'TournamentOBF'

