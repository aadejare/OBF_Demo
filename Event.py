#!/usr/bin/env python
import re, os, sys, time, shutil, json
from obsmodels import PROJECT_PATH, db, EventObf

class Event():
	# Initialize the data
	def __init__(self,eventDate=None,gameName=None,name=None,\
				numberEntrants=None, originURL=None, phaseID=None,\
				phases = None, ruleset=None,
				tournamentStructure=None, other=None):
		self.eventDate = eventDate
		self.gameName = gameName
		self.name = name
		self.numberEntrants = numberEntrants
		self.originURL = originURL
		self.phaseID = phaseID
		self.phases = phases
		self.ruleset = ruleset
		self.tournamentStructure = tournamentStructure
		self.other = other

    

	def saveeventinfo(self,savedata='update'):
		"""Save event information
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = EventObf.select().where(\
					EventObf.name==self.name)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				EInfo = EventObf.update(
		eventDate = self.eventDate,
		gameName = self.gameName,
		name = self.name,
		numberEntrants = self.numberEntrants,
		originURL = self.originURL,
		phaseID = self.phaseID,
		phases = self.phases,
		ruleset = self.ruleset,
		tournamentStructure = self.tournamentStructure,
		other = self.other
				).where(EventObf.name == self.name)
				EInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			EInfo = EventObf.create(
				eventDate = self.eventDate,
				gameName = self.gameName,
				name = self.name,
				numberEntrants = self.numberEntrants,
				originURL = self.originURL,
				phaseID = self.phaseID,
				phases = self.phases,
				ruleset = self.ruleset,
				tournamentStructure = self.tournamentStructure,
				other = self.other,
				tableid = str(secrets.token_hex(nbytes=16))
							)
			db.close()
		return 1
	def geteventinfo(self):
		"""Get player information
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = EventObf.select().where(EventObf.name == self.name)
		if query.exists():
			query = EventObf.select().where(\
					EventObf.name==self.name).get()
			return query
		else:
			return None
	def exporteventinfo(self):
		"""Export Event info into a dictonary
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		event_obj =  model_to_dict(self.geteventinfo())
		
# 		del event_obj['tableID'] # Delete table ID since it's not needed
		return event_obj
	def exporteventinfojson(self):
		"""Export Event info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		event_obj = self.exporteventinfo()
		return json.dumps(str({'Event':event_obj}))
		