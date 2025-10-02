#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import json
##This contains the demographics of the user which can be used to help customize the experience.
##Redundancies are made to ensure the reusability of the package
from obfmodels import db, PersonalInformationObf

class PersonalInformation():
	"""
	This is the class that stores and retrieves Personal Information data.
	"""
	# Initialize the data
	def __init__(self,name=None,entrant_language=None,gender=None, country=None, pronouns=None, \
	other=None,entrantTag=None, prefix=None):
		self.name = name
		self.country = country
		self.gender = gender
		self.pronouns=pronouns
		self.other = other
## Using entrant_ for a way to make sure that when parsing back the data it gets correctly labeled
		self.entrant_language = entrant_language
		self.prefix = prefix
		self.entrantTag = entrantTag

	def savepersonalinformation(self,savedata='update'):
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
		if type(self.other) == dict:
			self.other = json.dumps(self.other)
		query = PersonalInformationObf.select().where(\
					PersonalInformationObf.entrantTag==self.entrantTag)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				PInfo = PersonalInformationObf.update(
					country = self.country,
					gender = self.gender ,
					entrant_language = self.entrant_language,
					name = self.name,
					other = self.other,
					pronouns = self.pronouns,
					entrant_prefix = self.prefix,
					entrantTag = self.entrantTag,
				).where(PersonalInformationObf.entrantTag == self.entrantTag)
				PInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			PInfo = PersonalInformationObf.create(
				country = self.country,
				gender = self.gender ,
				entrant_language = self.entrant_language,
				name = self.name,
				other = self.other,
				pronouns = self.pronouns,
				entrant_prefix = self.prefix,
				entrantTag = self.entrantTag,
				tableid = secrets.token_hex(nbytes=16)

			)
			db.close()
		return 1
	def getpersonalinformation(self):
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
		# query = PersonalInformationObf.select().where(\
		# 			PersonalInformationObf.entrantTag == self.entrantTag)
		# if query.exists():
		# 	query = PersonalInformationObf.select().where(\
		# 			PersonalInformationObf.entrantTag == self.entrantTag).get()
		# 	db.close()
		# 	return query
		# else:
		# 	return None
		try:
			query = PersonalInformationObf.select().where(\
					PersonalInformationObf.entrantTag == self.entrantTag).get()
			db.close()
			return query
		except:
			return None
	def exportpersonalinformation(self):
		"""Export Player info into a dictonary

		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""
		from playhouse.shortcuts import model_to_dict, dict_to_model
		player_obj =  model_to_dict(self.getpersonalinformation())
		del player_obj['tableid'] # Delete table id since it's not needed
		player_obj['prefix'] = player_obj['entrant_prefix']
		player_obj['language'] = player_obj['entrant_language']
		del player_obj['entrant_prefix'], player_obj['entrant_language']
		player_obj['other'] = json.loads(player_obj['other'])
		return player_obj
	def exportpersonalinformationjsonstring(self):
		"""Export Player info into a json string

		:param none:
		:type: str
		:return: str
		"""
		player_obj = self.getpersonalinformation()
		return json.dumps(str({'personalInformation':player_obj}))
