#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import json
##This contains the demographics of the user which can be used to help customize the experience.
##Redundancies are made to ensure the reusability of the package
from obfmodels import db, PersonalInformationObf

class Character():
	"""
	This is the class that stores and retrieves character data.
	"""
	# Initialize the data
	def __init__(self,name=None,entrantCharacterName=None, entrantCharacterNameID=None):
		self.entrantCharacterName = TextField(column_name='entrantCharacterName', unique=True)
		self.entrantCharacterNameID = TextField(column_name='entrantCharacterNameID')

	def savecharacter(self,savedata='update'):
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

		query = CharacterObf.select().where(\
					CharacterObf.entrantCharacterName==self.entrantCharacterName,
					CharacterObf.entrantCharacterNameID==self.entrantCharacterNameID
					)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				CInfo = CharacterObf.update(
					entrantCharacterName = self.country,
					entrantCharacterNameID = self.gender ,
				).where(CharacterObf.entrantCharacterName==self.entrantCharacterName,
				CharacterObf.entrantCharacterNameID==self.entrantCharacterNameID)
				CInfo.execute()
				db.close()
				return 1
		else:
			CInfo = CharacterObf.update(
				entrantCharacterName = self.country,
				entrantCharacterNameID = self.gender ,
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
