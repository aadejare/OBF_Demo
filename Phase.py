#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import re, os, sys, time, shutil,json

from obsmodels import PROJECT_PATH, db, PhaseObf

class GamePhase():
	# Initialize the data
	def __init__(self,phaseID="",phaseStructure="",other=None):
		self.phaseID = phaseID
		self.phaseStructure = phaseStructure
		self.other = other
	def savephase(self,savedata='update'):
		"""Save phase information
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = PhaseObf.select().where(\
					PhaseObf.phaseID==self.phaseID)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				PPhase = PhaseObf.update(
					phaseID = self.phaseID,
					phaseStructure = self.phaseStructure ,
					other = self.other
				).where(PhaseObf.phaseID == self.phaseID)
				PPhase.execute()
				db.close()
				return 1
		else:
			PPhase = PhaseObf(
					phaseID = self.phaseID,
					phaseStructure = self.phaseStructure ,
					other = self.other
				)
			PPhase.save()
			db.close()
		return 1
	def getphase(self):
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
		query = PhaseObf.select().where(\
					PhaseObf.phaseID==self.phaseID)
		if query.exists():
			query = PhaseObf.select().where(\
					PhaseObf.phaseID==self.phaseID).get()
			return query
		else:
			return None
	def exportphase(self):
		"""Export Phase info into a dictonary
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		player_obj =  model_to_dict(self.getphase())
		del player_obj['tableid'] # Delete table id since it's not needed
		return player_obj
	def exportphasejson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		player_obj = self.exportphase()
		return json.dumps(str({'Phase':player_obj}))
		