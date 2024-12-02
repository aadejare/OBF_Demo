#!/usr/bin/env python
import re, os, sys, time, shutil,json

from obfmodels import PROJECT_PATH, db, GameObf, CharactersObf

	
class Game():
	# Initialize the data
	def __init__(self,gameNumber=None,entrant1Characters=None,entrant2Characters=None,\
				stage=None, entrant1Result=None,entrant2Result=None,setID=None,\
				other=None):
		# To save the data we will create a string from the list (array)
		# Encoded in ASCII and separated by commas
		self.entrant1Characters = entrant1Characters
		self.entrant2Characters= entrant2Characters
		self.entrant1Result=entrant1Result
		self.entrant2Result=entrant2Result
		self.gameNumber=gameNumber
		self.stage=stage
		self.setID = setID
		self.other = other

	def savegame(self,savedata='update'):
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = GameObf.select().where(\
					GameObf.gameNumber==self.gameNumber, GameObf.setID==self.setID)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				query = GameObf.select().where(\
					GameObf.gameNumber==self.gameNumber, GameObf.setID==self.setID).get()
					## Get the hashes
				entrant1hash = query.entrant1Characters
				entrant2hash = query.entrant2Characters
				GameInfo = GameObf.update(
						entrant1Characters=entrant1hash,
						entrant2Characters=entrant2hash,
						entrant1Result=self.entrant1Result,
						entrant2Result=self.entrant2Result,
						gameNumber=self.gameNumber,
						stage=self.stage,
						setID = self.setID,
						other=self.other
				).where(GameObf.gameNumber==self.gameNumber, GameObf.setID==self.setID)
				GameInfo.execute()
				eh_list =[]
				for i in self.entrant1Characters:
					eh_list.append({
					'entrantCharacterName': i,
					'entrantCharacterNameID': entrant1hash})
				for i in self.entrant2Characters:
					eh_list.append({
					'entrantCharacterName': i,
					'entrantCharacterNameID': entrant2hash})
				CharInfo = CharactersObf.delete().where(\
				CharactersObf.entrantCharacterNameID.in_(\
				[entrant1hash,entrant2hash])).execute()	
				CharInfo = CharactersObf.insert_many(eh_list)
				CharInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			entrant1hash = secrets.token_hex(nbytes=16)
			entrant2hash = secrets.token_hex(nbytes=16)
			GameInfo = GameObf.create(
						entrant1Characters=entrant1hash,
						entrant2Characters=entrant2hash,
						entrant1Result=self.entrant1Result,
						entrant2Result=self.entrant2Result,
						gameNumber=self.gameNumber,
						setID = self.setID,
						stage=self.stage,
						other=self.other,
						tableid = secrets.token_hex(nbytes=16)	
				)
			#Entrance dictionary for inserts
			eh_list =[]
			for i in self.entrant1Characters:
				eh_list.append({
				'entrantCharacterName': i,
				'entrantCharacterNameID': entrant1hash})
			for i in self.entrant2Characters:
				eh_list.append({
				'entrantCharacterName': i,
				'entrantCharacterNameID': entrant2hash})
			CharInfo = CharactersObf.insert_many(eh_list)
			CharInfo.execute()
			db.close()
		return 1
	def getgame(self):
		"""Get game information
		
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
					GameObf.gameNumber==self.gameNumber, GameObf.setID==self.setID)
		if query.exists():
			query = GameObf.select(\
			GameObf.gameNumber, GameObf.entrant1Characters, GameObf.entrant2Characters,\
				GameObf.stage, GameObf.entrant1Result, GameObf.entrant2Result\
			).where(\
					GameObf.gameNumber==self.gameNumber, GameObf.setID==self.setID).get()
			entrant1list = []
			entrant2list = []
			entrant1hash = query.entrant1Characters.decode("utf-8")
			entrant2hash = query.entrant2Characters.decode("utf-8")
			CharInfo = CharactersObf.select().where(\
				CharactersObf.entrantCharacterNameID.in_(\
				[str(entrant1hash),str(entrant2hash)]))
			CharInfo.execute()	
			for i in CharInfo:
				if i.entrantCharacterNameID == str(entrant1hash):
					entrant1list.append(i.entrantCharacterName)
				else:
					entrant2list.append(i.entrantCharacterName)
			query.entrant1Characters = entrant1list
			query.entrant2Characters = entrant2list
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
		del game_obj['tableid'] # Delete table id since it's not needed
		del game_obj['setID'] # Delete set ID since it's not needed
		return game_obj
	def exportgamejson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		game_obj = self.exportgame()
		return json.dumps(str({'Set':game_obj}))
	def exportgames(self):
		"""Export the list of games
		:param none:
		:type: str
		:return: list
		"""
		from playhouse.shortcuts import model_to_dict
		gameslist = []
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = GameObf.select().where(GameObf.setID==self.setID)\
			.order_by(GameObf.gameNumber)
		if query.exists():
			query = GameObf.select(GameObf.gameNumber, GameObf.setID).where(\
					 GameObf.setID==self.setID).order_by(GameObf.gameNumber)
		for ix in query:
			game_subquery = GameObf.select(\
			GameObf.gameNumber, GameObf.entrant1Characters, GameObf.entrant2Characters,\
				GameObf.stage, GameObf.entrant1Result, GameObf.entrant2Result).where(\
					GameObf.gameNumber==ix.gameNumber, GameObf.setID==ix.setID).get()
			entrant1list = []
			entrant2list = []
			entrant1hash = game_subquery.entrant1Characters.decode("utf-8")
			entrant2hash = game_subquery.entrant2Characters.decode("utf-8")
			CharInfo = CharactersObf.select().where(\
				CharactersObf.entrantCharacterNameID.in_(\
				[str(entrant1hash),str(entrant2hash)]))
			CharInfo.execute()	
			for i in CharInfo:
				if i.entrantCharacterNameID == str(entrant1hash):
					entrant1list.append(i.entrantCharacterName)
				else:
					entrant2list.append(i.entrantCharacterName)
			game_subquery.entrant1Characters = entrant1list
			game_subquery.entrant2Characters = entrant2list
			game_subquery_obj =  model_to_dict(game_subquery)
			del game_subquery_obj['tableid'] # Delete table id since it's not needed
			del game_subquery_obj['setID'] # Delete set ID since it's not needed
			gameslist.append(game_subquery_obj)
			db.close()
		return gameslist