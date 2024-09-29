#!/usr/bin/env python
import re, os, sys, time, shutil,json

from obsmodels import PROJECT_PATH, db, GameObf

	
class Game():
	# Initialize the data
	def __init__(self,gameNumber=None,entrant1Characters=None,entrant2Characters=None,\
				stage=None, entrant1Result=None,entrant2Result=None,\
				other=None):
		# To save the data we will create a string from the list (array)
		# Encoded in ASCII and separated by commas
		self.entrant1Characters = entrant1Characters
		self.entrant2Characters= entrant2Characters
		self.entrant1Result=entrant1Result
		self.entrant2Result=entrant2Result
		self.gameNumber=gameNumber
		self.stage=stage
		self.other = other

	def savegame(self,savedata='update'):
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = GameObf.select().where(\
					GameObf.gameNumber==self.gameNumber)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				GameInfo = GameObf.update(
						entrant1Characters=\
									",".join(map(str, self.entrant1Characters)).encode('ASCII'),
						entrant2Characters=\
									",".join(map(str, self.entrant2Characters)).encode('ASCII'),
						entrant1Result=self.entrant1Result,
						entrant2Result=self.entrant2Result,
						gameNumber=self.gameNumber,
						stage=self.stage,
						other=self.other
				).where(GameObf.gameNumber==self.gameNumber)
				GameInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			GameInfo = GameObf.create(
						entrant1Characters=self.entrant1Characters,
						entrant2Characters=self.entrant2Characters,
						entrant1Result=self.entrant1Result,
						entrant2Result=self.entrant2Result,
						gameNumber=self.gameNumber,
						stage=self.stage,
						other=self.other,
						tableid = str(secrets.token_hex(nbytes=16))	
				)
			db.close()
		return 1
	def getgame(self):
		"""Get phase information
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = GameObf.select().where(\
					GameObf.gameNumber==self.gameNumber)
		if query.exists():
			query = GameObf.select().where(\
					GameObf.gameNumber==self.gameNumber).get()

			return query
		else:
			return None
	def exportgame(self):
			"""Export Set info into a dictonary
		
			:param savedata: Method of saving the data new is new data, rewrite is rewriting data
			:type: str
			:return: dict
			"""	
			from playhouse.shortcuts import model_to_dict, dict_to_model
			game_obj =  model_to_dict(self.getgame())
			game_obj['entrant1Characters'] = \
				[i for i in game_obj['entrant1Characters'].decode('utf-8').split(',')]
			game_obj['entrant2Characters'] = \
				[i for i in game_obj['entrant2Characters'].decode('utf-8').split(',')]
			del game_obj['tableid'] # Delete table id since it's not needed
			return game_obj
	def exportgamejson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		game_obj = self.exportgame()
		return json.dumps(str({'Set':game_obj}))