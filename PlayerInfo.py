#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import re, os, sys, time, shutil, numpy, cgi, cgitb, json
##This contains the demographics of the user which can be used to help customize the experience.
##Redundancies are made to ensure the reusability of the package
from obsmodels import PROJECT_PATH, db, PersonalInformationObf

class PlayerInfo():
	# Initialize the data
	def __init__(self,name=None,language=None,gender=None, country=None, pronouns=None, other=None):
		self.name = name
		self.country = country
		self.gender = gender
		self.pronouns=pronouns
		self.other = other
		self.language = language

	def saveplayerinfo(self,savedata='update'):
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
					PersonalInformationObf.name==self.name)
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
				).where(PersonalInformationObf.name == self.name)
				PInfo.execute()
				db.close()
				return 1
		else:
			PInfo = PersonalInformationObf(
				country = self.country,
				gender = self.gender ,
				language = self.language ,
				name = self.name,
				other = self.other,
				pronouns = self.pronouns ,
			)
			PInfo.save()
			db.close()
		return 1
	def getplayerinfo(self):
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
					PersonalInformationObf.name==self.name)
		if query.exists():
			query = PersonalInformationObf.select().where(\
					PersonalInformationObf.name==self.name).get()
			return query
		else:
			return None
	def exportplayerinfo(self):
		from playhouse.shortcuts import model_to_dict, dict_to_model
		player_obj =  model_to_dict(self.getplayerinfo())
		## Multiple fetches use this 
		#https://stackoverflow.com/questions/21975920/peewee-model-to-json
		# users = list(User.select().where(User.name ** 'a%').dicts()) 
		del player_obj['tableid'] # Delete table id since it's not needed
		return json.dumps(str({'personalInformation':player_obj}))
		