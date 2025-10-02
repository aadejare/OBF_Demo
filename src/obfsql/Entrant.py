#!/usr/bin/env python
import json
from obfmodels import db, EntrantObf, PersonalInformationObf
from PersonalInformation import PersonalInformation

class Entrant():
	# Initialize the data
	def __init__(self,entrantTag=None,entrantID=None,finalPlacement=None,\
				initialSeed=None, personalInformation = None, 
				tournamentID=None, entrantTeam='None', other=None):
		self.entrantTag = entrantTag
		self.entrantID = entrantID
		self.entrantTeam = entrantTeam
		self.finalPlacement = finalPlacement
		self.initialSeed = initialSeed
		self.other = other
		self.personalInformation = personalInformation
		self.tournamentID = tournamentID
    

	def saveentrant(self,savedata='update'):
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
					EntrantObf.entrantTag==self.entrantTag,
					EntrantObf.tournamentID == self.tournamentID)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				# Break the PI data into dictionary form
				pi_dict = self.personalInformation[0]
				# Try and catch for data
				pifields = ['name','gender','country','pronouns','tag','prefix', 'language','other']
				for pif in pifields:
					if pif not in pi_dict.keys():
						pi_dict[pif] = None
				## Save PI first then Entrant data
				PI_Data = PersonalInformation(
				name=pi_dict['name'],
				country=pi_dict['country'],
				gender=pi_dict['gender'],
				prefix=pi_dict['prefix'],
				pronouns=pi_dict['pronouns'],
				other=pi_dict['other'],
				entrant_language =pi_dict['language'],
				entrantTag=self.entrantTag)
				if PI_Data.savepersonalinformation('new') == -1:
					PI_Data.savepersonalinformation() 
				if type(self.other) == dict:
					self.other = json.dumps(self.other)
				EInfo = EntrantObf.update(
					entrantID = self.entrantID,
					entrantTag = self.entrantTag,
					entrantTeam = self.entrantTeam,
					finalPlacement = self.finalPlacement,
					initialSeed = self.initialSeed,
					other = self.other,
					tournamentID = self.tournamentID
				).where(EntrantObf.entrantTag == self.entrantTag,
						EntrantObf.tournamentID == self.tournamentID)
				EInfo.execute()
				db.close()
				return 1
		else:
			import secrets
			# Break the PI data into dictionary form
			pi_dict = self.personalInformation[0]
			## Save PI first then Entrant data
			pifields = ['name','gender','country','pronouns','tag','prefix', 'language','other']
			for pif in pifields:
				if pif not in pi_dict.keys():
					pi_dict[pif] = None
			PI_Data = PersonalInformation(
			name=pi_dict['name'],
			country=pi_dict['country'],
			gender=pi_dict['gender'],
			prefix=pi_dict['prefix'],
			pronouns=pi_dict['pronouns'],
			other=pi_dict['other'],
			entrant_language =pi_dict['language'],
			entrantTag=self.entrantTag)
			if PI_Data.savepersonalinformation('new') == -1:
				PI_Data.savepersonalinformation() 
			if type(self.other) == dict:
				self.other = json.dumps(self.other)
			EInfo = EntrantObf.create(
						entrantID = self.entrantID,
						entrantTag = self.entrantTag,
						entrantTeam = self.entrantTeam,
						finalPlacement = self.finalPlacement,
						initialSeed = self.initialSeed,
						other = self.other,
						tournamentID = self.tournamentID,
						tableid = secrets.token_hex(nbytes=16)
							)
			db.close()
		return 1
	def getentrant(self):
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
					EntrantObf.entrantTag==self.entrantTag,
					EntrantObf.tournamentID == self.tournamentID)
		if query.exists():
			query = EntrantObf.select().where(\
					EntrantObf.entrantTag==self.entrantTag,
					EntrantObf.tournamentID == self.tournamentID).get()
			return query
		else:
			return None
	def exportentrant(self):
		"""Export Player info into a dictonary
		
		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""	
		from playhouse.shortcuts import model_to_dict, dict_to_model
		entrant_obj =  model_to_dict(self.getentrant())
		entrant_obj['other'] = json.loads(entrant_obj['other'] )
		del entrant_obj['tableid'] # Delete table id since it's not needed
		del entrant_obj['tournamentID'] # Delete tournament ID since it's not needed

		return entrant_obj
	def exportentrantjsonstring(self):
		"""Export Player info into a json string
		
		:param none: 
		:type: str
		:return: str
		"""	
		entrant_obj = self.exportentrant()
		return json.dumps(str({'Entrant':entrant_obj}))
	def exportentrants(self):
		"""Export the list of entrants and their personal infomation
		:param none:
		:type: str
		"""
		from playhouse.shortcuts import model_to_dict
		entrantslist = []
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = EntrantObf.select().where(\
					EntrantObf.tournamentID == self.tournamentID)\
					.order_by(EntrantObf.entrantTag)
		if query.exists(): #Check to see if it's none
			query = EntrantObf.select().where(\
					EntrantObf.tournamentID == self.tournamentID)\
					.order_by(EntrantObf.entrantTag)
		else:
			db.close()
			return None
		looper = -1
		for ix in query:
			looper+=1
# 			print("Hello: " + str(ix.entrantTag))
			entrant_subquery = EntrantObf.select( EntrantObf.entrantID,
				EntrantObf.entrantTag,EntrantObf.finalPlacement,\
				EntrantObf.initialSeed, 
				EntrantObf.entrantTeam, EntrantObf.other\
				).where(EntrantObf.entrantTag==ix.entrantTag,
					EntrantObf.tournamentID == ix.tournamentID).get()
			PI_Data = PersonalInformation(entrant_tag =ix.entrantTag)
			pi_export =  PI_Data.exportpersonalinformation()
### Because PI closes the database we need to open the db again
			entrant_subquery_obj =  model_to_dict(entrant_subquery)
			entrant_subquery_obj['other'] = json.loads(entrant_subquery_obj['other'])
			entrant_subquery_obj['personalInformation'] = [pi_export]
			entrantslist.append(entrant_subquery_obj)
		return entrantslist