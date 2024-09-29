#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import re, os, sys, time, shutil, json
##This contains the demographics of the user which can be used to help customize the experience.
##Redundancies are made to ensure the reusability of the package
from obsmodels import PROJECT_PATH, db, PersonalInformationObf

class PersonalInformation():
	# Initialize the data
	def __init__(self,name=None,language=None,gender=None, country=None, pronouns=None, \
	other=None,entrant_tag=None):
		self.name = name
		self.country = country
		self.gender = gender
		self.pronouns=pronouns
		self.other = other
		self.language = language
		self.entrant_tag = entrant_tag

	def savepersonalinformationinfo(self,savedata='update'):
		"""Save player information
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""	
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = PersonalInformationObf.select().where(\
					PersonalInformationObf.entrant_tag==self.entrant_tag)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				PInfo = PersonalInformationObf.update(
					country = self.country,
					gender = self.gender ,
					language = self.language ,
					name = self.name,
					other = self.other,
					pronouns = self.pronouns ,
					entrant_tag = self.entrant_tag,
				).where(PersonalInformationObf.entrant_tag == self.entrant_tag)
				PInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			PInfo = PersonalInformationObf.create(
				country = self.country,
				gender = self.gender ,
				language = self.language ,
				name = self.name,
				other = self.other,
				pronouns = self.pronouns ,
				entrant_tag = self.entrant_tag,
				tableid = str(secrets.token_hex(nbytes=16))
			)
			db.close()
		return 1
	def getpersonalinformationinfo(self):
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
		query = PersonalInformationObf.select().where(\
					PersonalInformationObf.entrant_tag == self.entrant_tag)
		if query.exists():
			query = PersonalInformationObf.get(\
					PersonalInformationObf.entrant_tag == self.entrant_tag)
			return query
		else:
			return None
	def exportpersonalinformationinfo(self):
		"""Export Player info into a dictonary
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		player_obj =  model_to_dict(self.getpersonalinformationinfo())
		del player_obj['tableid'] # Delete table id since it's not needed
		return player_obj
	def exportpersonalinformationinfojson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		player_obj = self.exportpersonalinformationinfo()
		return json.dumps(str({'personalInformation':player_obj}))
		