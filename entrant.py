#!/usr/bin/env python
##Build using Bootstrap, Flask, Flask-WTForms
import re, os, sys, time, shutil, json
##This contains the demographics of the user which can be used to help customize the experience.
##Redundancies are made to ensure the reusability of the package
from obsmodels import PROJECT_PATH, db, EntrantObf

class Entrant():
	# Initialize the data
	def __init__(self,entrant_tag=None,entrant_team=None,final_placement=None,\
				initial_seed=None, setID=None, personalInformation = None, other=None):
		self.entrant_tag = entrant_tag
		self.entrant_team = entrant_team
		self.final_placement = final_placement
		self.initial_seed = initial_seed
		self.other = other
		self.personalInformation = personalInformation
		self.setID = setID
    

	def saveentrantinfo(self,savedata='update'):
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
		query = EntrantObf.select().where(\
					EntrantObf.entrant_tag==self.entrant_tag)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				EInfo = EntrantObf.update(
					entrant_tag = self.entrant_tag,
					entrant_team = self.entrant_team,
					final_placement = self.final_placement,
					initial_seed = self.initial_seed,
					other = self.other,
					personalInformation = self.personalInformation,
					setID = self.setID,
				).where(EntrantObf.entrant_tag == self.entrant_tag)
				EInfo.execute()
				db.close()
				return 1
		else:
			EInfo = EntrantObf(
						entrant_tag = self.entrant_tag,
						entrant_team = self.entrant_team,
						final_placement = self.final_placement,
						initial_seed = self.initial_seed,
						other = self.other,
						personalInformation = self.personalInformation,
						setID = self.setID,
							)
			EInfo.save()
			db.close()
		return 1
	def getentrantinfo(self):
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
		query = EntrantObf.select().where(\
					EntrantObf.entrant_tag==self.entrant_tag)
		if query.exists():
			query = EntrantObf.select().where(\
					EntrantObf.entrant_tag==self.entrant_tag).get()
			return query
		else:
			return None
	def exportentrantinfo(self):
		"""Export Player info into a dictonary
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		entrant_obj =  model_to_dict(self.getentrantinfo())
		del entrant_obj['tableid'] # Delete table id since it's not needed
		return entrant_obj
	def exportentrantinfojson(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		entrant_obj = self.exportentrantinfo()
		return json.dumps(str({'Entrant':entrant_obj}))
		