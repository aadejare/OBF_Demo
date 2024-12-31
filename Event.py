#!/usr/bin/env python
import re, os, sys, time, shutil, json
from obfmodels import db, EventObf

class Event():
	# Initialize the data
	def __init__(self,eventDate=None,gameName=None,name=None,\
				numberEntrants=None, originURL=None, ruleset=None,\
				tournamentStructure=None, 
				tournamentID = None, other=None):
		self.eventDate = eventDate
		self.gameName = gameName
		self.name = name
		self.numberEntrants = numberEntrants
		self.originURL = originURL
		self.ruleset = ruleset
		self.tournamentStructure = tournamentStructure
		self.tournamentID = tournamentID
		self.other = other

	def saveevent(self,savedata='update'):
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
					EventObf.name==self.name, EventObf.tournamentID==self.tournamentID)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				query = EventObf.select().where(\
					EventObf.name==self.name, EventObf.tournamentID==self.tournamentID)\
					.get()
				tablehash = query.tableid
				EInfo = EventObf.update(
					eventDate = self.eventDate,
					gameName = self.gameName,
					name = self.name,
					numberEntrants = self.numberEntrants,
					originURL = self.originURL,
					ruleset = self.ruleset,
					tournamentStructure = self.tournamentStructure,
					other = self.other,
					tournamentID = self.tournamentID,
					tableid = tablehash
							).where(EventObf.name == self.name,EventObf.tournamentID==self.tournamentID)
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
				ruleset = self.ruleset,
				tournamentStructure = self.tournamentStructure,
				other = self.other,
				tournamentID = self.tournamentID,
				tableid = secrets.token_hex(nbytes=16)
							)
			db.close()
		return 1
	def getevent(self):
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
		query = EventObf.select().where(EventObf.name==self.name, \
					EventObf.tournamentID==self.tournamentID)
		if query.exists():
			query = EventObf.select().where(\
					EventObf.name==self.name, EventObf.tournamentID==self.tournamentID).get()
			return query
		else:
			return None
	def exportevent(self):
		"""Export Event info into a dictonary
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		event_obj =  model_to_dict(self.getevent())
		
		del event_obj['tableid'] # Delete table ID since it's not needed
		return event_obj
	def exporteventjson(self):
		"""Export Event info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		event_obj = self.exportevent()
		return json.dumps(str({'Event':event_obj}))
		