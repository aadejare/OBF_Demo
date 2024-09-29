#!/usr/bin/env python
import re, os, sys, time, shutil,json

from obsmodels import PROJECT_PATH, db, SetObf
#Called MatchSet because SET is a reserved word in Python


class MatchSet():
	# Initialize the data
	def __init__(self,setID=None, entrant1ID=None,entrant2ID=None, status=None,\
				entrant1Result=None,entrant2Result=None,\
				entrant1Score=None, entrant2Score=None,
				winnerNextSetID=None, loserNextSetID=None,
				entrant1PrevSetID=None, entrant2PrevSetID=None,
				setFormat=None, phaseID=None,roundID=None, games=None, other=None):
		self.setID = setID
		self.entrant1ID=entrant1ID
		self.entrant2ID=entrant2ID
		self.status=status
		self.entrant1Result=entrant1Result
		self.entrant2Result=entrant2Result
		self.entrant1Score=entrant1Score
		self.entrant2Score=entrant2Score
		self.winnerNextSetID=winnerNextSetID
		self.loserNextSetID=loserNextSetID
		self.entrant1PrevSetID=entrant1PrevSetID
		self.entrant2PrevSetID=entrant2PrevSetID
		self.setFormat=setFormat
		self.phaseID=phaseID
		self.roundID=roundID
		self.games=games
		self.other = other

	def saveset(self,savedata='update'):
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = SetObf.select().where(\
					SetObf.setID==self.setID)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				SETInfo = SetObf.update(
					setID=self.setID,
					entrant1ID=self.entrant1ID,
					entrant2ID=self.entrant2ID,
					status=self.status,
					entrant1Result=self.entrant1Result,
					entrant2Result=self.entrant2Result,
					entrant1Score=self.entrant1Score,
					entrant2Score=self.entrant2Score,
					winnerNextSetID=self.winnerNextSetID,
					loserNextSetID=self.loserNextSetID,
					entrant1PrevSetID=self.entrant1PrevSetID,
					entrant2PrevSetID=self.entrant2PrevSetID,
					setFormat=self.setFormat,
					phaseID=self.phaseID,
					roundID=self.roundID,
					games=self.games,
					other=self.other,
				).where(SetObf.setID==self.setID)
				SETInfo.execute()
				db.close()
				return 1
		else:
			SETInfo = SetObf(
					setID=self.setID,
					entrant1ID=self.entrant1ID,
					entrant2ID=self.entrant2ID,
					status=self.status,
					entrant1Result=self.entrant1Result,
					entrant2Result=self.entrant2Result,
					entrant1Score=self.entrant1Score,
					entrant2Score=self.entrant2Score,
					winnerNextSetID=self.winnerNextSetID,
					loserNextSetID=self.loserNextSetID,
					entrant1PrevSetID=self.entrant1PrevSetID,
					entrant2PrevSetID=self.entrant2PrevSetID,
					setFormat=self.setFormat,
					phaseID=self.phaseID,
					roundID=self.roundID,
					games=self.games,
					other=self.other,
				)
			SETInfo.save()
			db.close()
		return 1
	def getset(self):
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
		query = SetObf.select().where(\
					SetObf.setID==self.setID)
		if query.exists():
			query = SetObf.select().where(\
					SetObf.setID==self.setID).get()
			return query
		else:
			return None
	def exportset(self):
			"""Export Set info into a dictonary
		
			:param savedata: Method of saving the data new is new data, rewrite is rewriting data
			:type: str
			:return: dict
			"""	
			from playhouse.shortcuts import model_to_dict, dict_to_model
			player_obj =  model_to_dict(self.getset())
			del player_obj['tableid'] # Delete table id since it's not needed
			return player_obj
	def exportphasejson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		player_obj = self.exportset()
		return json.dumps(str({'Set':player_obj}))