#!/usr/bin/env python
import json

from obfmodels import db, TournamentObf
# To change databse alter, changedb

class Tournament():
	"""
	This is the class that stores and retrieves Tournament data.
	Note: tournamentTitle is the substitue for title in OBF. Since title is a reserved word in SQL
	and python for strings, it helps to remove confusion
	"""
	# Initialize the data
	def __init__(self,tournamentTitle=None,SetGameResult=None,description=None,\
				tournamentID=None, obfversion=None):
		# To save the data we will create a string from the list (array)
		# Encoded in ASCII and separated by commas
		self.tournamentTitle = tournamentTitle
		self.obfversion = obfversion
		self.SetGameResult=SetGameResult
		self.tournamentID=tournamentID
		self.description=description
	def savetournament(self,savedata='update'):
		if self.tournamentID is None and savedata == 'update':
			return -1
		try:
			db.connect()
		except:
			db.close()
			db.connect()
		if savedata == 'update':
			try:
				TourInfo = TournamentObf.update(
						tournamentTitle=self.tournamentTitle,
						obfversion=self.obfversion,
						SetGameResult=json.dumps(self.SetGameResult),
						tournamentID=self.tournamentID,
						description=self.description
				).where(TournamentObf.tournamentID==self.tournamentID)
				TourInfo.execute()
				db.close()
				return 1
			except:
				# Failed to fetch
				return 0
		else:
			import secrets
# If there's no tournament ID and it's a new save, then we generate one for them
			if self.tournamentID is None:
				self.tournamentID  = secrets.token_hex(nbytes=16)
			TourInfo = TournamentObf.create(
					tournamentTitle=self.tournamentTitle,
					obfversion=self.obfversion,
					SetGameResult=json.dumps(self.SetGameResult),
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
		try:
			query = TournamentObf.select(\
			TournamentObf.tournamentTitle, TournamentObf.description, TournamentObf.SetGameResult,\
				TournamentObf.obfversion, TournamentObf.tournamentID
			).where(\
					TournamentObf.tournamentID==self.tournamentID).get()
			return query
		except:
			return None
	def gettournamentID(self):
		"""Get game information

		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""
		if self.tournamentTitle is None:
			return -1
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		try:
			query = TournamentObf.select(TournamentObf.tournamentTitle,\
			TournamentObf.tournamentID).where(\
					TournamentObf.tournamentTitle==self.tournamentTitle)
			self.tournamentID = list(query)[-1].tournamentID
			return 0
		except:
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
		tourn_obj['SetGameResult'] = json.loads(tourn_obj['SetGameResult'])
		tourn_obj['version'] = tourn_obj['obfversion']
		#Delete the following since we don't need them anymore
		del tourn_obj['tournamentTitle'], tourn_obj['obfversion'], tourn_obj['tableid']
		return tourn_obj
	def exporttournamentjson(self):
		"""Export Player info into a json string

		:param none:
		:type: str
		:return: str
		"""
		tourn_obj = self.exporttournament()
		return json.dumps(str({'Tournament':tourn_obj}))
