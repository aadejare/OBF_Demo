#!/usr/bin/env python
import re, os, sys, time, shutil,json

from obfmodels import PROJECT_PATH, db, TournamentObf
	
	
class Tournament():
	"""
	tournamentTitle is the substitue for title in OBF. Since title is a reserved word in SQ
	and python for strings, it helps to remove confusion
	"""
	# Initialize the data
	def __init__(self,tournamentTitle=None,description=None,definitions=None,\
				tournamentID=None, obfversion=None):
		# To save the data we will create a string from the list (array)
		# Encoded in ASCII and separated by commas
		self.tournamentTitle = tournamentTitle
		self.obfversion = obfversion
		self.definitions=definitions
		self.tournamentID=tournamentID
		self.description=description
	def savetournament(self,savedata='update'):
		if self.tournamentID is None and savedata == 'update':
			return -1
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = TournamentObf.select().where(\
					TournamentObf.tournamentID==self.tournamentID)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				query = TournamentObf.select().where(\
					TournamentObf.tournamentID==self.tournamentID).get()
					## Get the hashes
				TourInfo = TournamentObf.update(
						tournamentTitle=self.tournamentTitle,
						obfversion=self.obfversion,
						definitions=json.dumps(self.definitions),
						tournamentID=self.tournamentID,
						description=self.description

				).where(TournamentObf.tournamentID==self.tournamentID)
				TourInfo.execute()
				db.close()
				return 1
		else:
			import secrets
# If there's no tournament ID and it's a new save, then we generate one for them
			if self.tournamentID is None:
				self.tournamentID  = secrets.token_hex(nbytes=16)
			TourInfo = TournamentObf.create(
					tournamentTitle=self.tournamentTitle,
					obfversion=self.obfversion,
					definitions=json.dumps(self.definitions),
					tournamentID=self.tournamentID,
					description=self.description,
					tableid = secrets.token_hex(nbytes=16)
				)
			db.close()
		return 1
	def gettournament(self):
		"""Get game information
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""	
		if self.tournamentID is None:
			return -1
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = TournamentObf.select().where(\
					TournamentObf.tournamentID==self.tournamentID)

		if query.exists():
			query = TournamentObf.select(\
			TournamentObf.tournamentTitle, TournamentObf.description, TournamentObf.definitions,\
				TournamentObf.obfversion, TournamentObf.tournamentID
			).where(\
					TournamentObf.tournamentID==self.tournamentID).get()
			return query
		else:
			return None
	def exporttournament(self):
		"""Export Set info into a dictonary
	
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		tourn_obj =  model_to_dict(self.gettournament())
		tourn_obj['title'] = tourn_obj['tournamentTitle']
		tourn_obj['definitions'] = json.loads(tourn_obj['definitions'])
		del tourn_obj['tournamentTitle']
		del tourn_obj['tableid']
		return tourn_obj
	def exporttournamentjson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		tourn_obj = self.exporttournament()
		return json.dumps(str({'Tournament':tourn_obj}))