#!/usr/bin/env python
import json

from obfmodels import  db, SetObf
#Called MatchSet because SET is a reserved word in Python


class MatchSet():
	# Initialize the data
	def __init__(self,setID=None, entrant1ID=None,entrant2ID=None, status=None,\
				entrant1Result=None,entrant2Result=None,\
				entrant1Score=None, entrant2Score=None,
				entrant1NextSetID=None, entrant2NextSetID=None,
				entrant1PrevSetID=None, entrant2PrevSetID=None,
				setFormat=None, phaseID=None,roundID=None, games=None, 
				tournamentID=None, other=None):
		self.setID = setID #Assume that SetID is unique
		self.entrant1ID=entrant1ID
		self.entrant2ID=entrant2ID
		self.status=status
		self.entrant1Result=entrant1Result
		self.entrant2Result=entrant2Result
		self.entrant1Score=entrant1Score
		self.entrant2Score=entrant2Score
		self.entrant1NextSetID=entrant1NextSetID
		self.entrant2NextSetID=entrant2NextSetID
		self.entrant1PrevSetID=entrant1PrevSetID
		self.entrant2PrevSetID=entrant2PrevSetID
		self.setFormat=setFormat
		self.phaseID=phaseID
		self.roundID=roundID
		self.games=games
		self.tournamentID = tournamentID
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
				query = SetObf.select().where(\
					SetObf.setID==self.setID, 
					SetObf.tournamentID==self.tournamentID).get()
				tablehash = query.tableid
				SETInfo = SetObf.update(
					setID=self.setID,
					entrant1ID=self.entrant1ID,
					entrant2ID=self.entrant2ID,
					status=self.status,
					entrant1Result=self.entrant1Result,
					entrant2Result=self.entrant2Result,
					entrant1Score=self.entrant1Score,
					entrant2Score=self.entrant2Score,
					entrant1NextSetID=self.entrant1NextSetID,
					entrant2NextSetID=self.entrant2NextSetID,
					entrant1PrevSetID=self.entrant1PrevSetID,
					entrant2PrevSetID=self.entrant2PrevSetID,
					setFormat=self.setFormat,
					phaseID=self.phaseID,
					roundID=self.roundID,
					games=self.games,
					tournamentID=self.tournamentID,
					tableid = tablehash,
					other=self.other,
				).where(SetObf.setID==self.setID, SetObf.tournamentID==self.tournamentID)
				SETInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			sethash = secrets.token_hex(nbytes=16)
			SETInfo = SetObf(
					setID=self.setID,
					entrant1ID=self.entrant1ID,
					entrant2ID=self.entrant2ID,
					status=self.status,
					entrant1Result=self.entrant1Result,
					entrant2Result=self.entrant2Result,
					entrant1Score=self.entrant1Score,
					entrant2Score=self.entrant2Score,
					entrant1NextSetID=self.entrant1NextSetID,
					entrant2NextSetID=self.entrant2NextSetID,
					entrant1PrevSetID=self.entrant1PrevSetID,
					entrant2PrevSetID=self.entrant2PrevSetID,
					setFormat=self.setFormat,
					phaseID=self.phaseID,
					roundID=self.roundID,
					games=self.games,
					tournamentID=self.tournamentID,
					tableid = sethash,
					other=self.other,
				)
			SETInfo.save(force_insert=True)
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
					SetObf.setID==self.setID, SetObf.tournamentID==self.tournamentID)
		if query.exists():
			query = SetObf.select().where(\
					SetObf.setID==self.setID, SetObf.tournamentID==self.tournamentID).get()
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
		set_obj =  model_to_dict(self.getset())
		del set_obj['tableid'] # Delete table id since it's not needed
		del set_obj['tournamentID'] # Delete tournament ID since it's not needed
		return set_obj
	def exportsets(self):
		"""Export Set info into a dictonary
	
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		setlist=[] #Yes list of set is called set list
		from playhouse.shortcuts import model_to_dict, dict_to_model
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = SetObf.select().where(\
					SetObf.tournamentID==self.tournamentID)
		if query.exists():
			query = SetObf.select().where(\
					SetObf.tournamentID==self.tournamentID).order_by(SetObf.setID)
		for ix in query:
			set_obj =  model_to_dict(ix)
			del set_obj['tableid'], set_obj['tournamentID'] # Delete table id since it's not needed
			setlist.append(set_obj)
		return setlist

	def exportphasejsonstring(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		set_obj = self.exportset()
		return json.dumps(str({'Set':set_obj}))