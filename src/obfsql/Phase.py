#!/usr/bin/env python
import re, os, sys, time, shutil,json

from obfmodels import db, PhaseObf

class Phase():
	"""
	This is the class that stores and retrieves Phase data.
	"""
	# Initialize the data
	def __init__(self,phaseID=None,phaseStructure=None, eventID=None,name=None,other=None):
		self.phaseID = phaseID
		self.phaseStructure = phaseStructure
		self.eventID = eventID
		self.name=name
		self.other = other
	def savephase(self,savedata='update'):
		"""Save phase information

		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = PhaseObf.select().where(\
					PhaseObf.phaseID==self.phaseID, PhaseObf.name==self.name)
		if query.exists():
			if savedata == 'new':
				return -1
			else:
				if type(self.other) == dict:
					self.other = json.dumps(self.other)
				PPhase = PhaseObf.update(
					phaseID = self.phaseID,
					phaseStructure = self.phaseStructure ,
					eventID = self.eventID,
					name=self.name,
					other = self.other
				).where(PhaseObf.phaseID == self.phaseID, PhaseObf.name==self.name)
				PPhase.execute()
				db.close()
				return 1
		else:
			if type(self.other) == dict:
				self.other = json.dumps(self.other)
			PPhase = PhaseObf(
					phaseID = self.phaseID,
					phaseStructure = self.phaseStructure ,
					eventID = self.eventID,
					name=self.name,
					other = self.other
				)
			PPhase.save()
			db.close()
		return 1
	def getphase(self):
		"""Get phase information

		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: boolean
		"""
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		query = PhaseObf.select().where(\
					PhaseObf.phaseID==self.phaseID)
		if query.exists():
			query = PhaseObf.select().where(\
					PhaseObf.phaseID==self.phaseID).get()
			return query
		else:
			return None
	def exportphase(self):
		"""Export Phase info into a dictonary

		:param savedata: Method of saving the data new is new data, rewrite is rewriting data
		:type: str
		:return: dict
		"""
		from playhouse.shortcuts import model_to_dict, dict_to_model
		phase_obj =  model_to_dict(self.getphase())
		del phase_obj['tableid'], phase_obj['name'] # Delete table id since it's not needed
		## For now we will delete eventID but plan for it in the future
		del phase_obj['eventID']
		phase_obj['other'] = json.loads(phase_obj['other'])
		return phase_obj
	def exportphases(self):
		"""Export the list of phases
		:param none:
		:type: str
		:return: list
		"""
		from playhouse.shortcuts import model_to_dict
		phaseslist = []
		try:
			db.connect()
		except Exception as e:
			db.close()
			db.connect()
		# For right now querying on event name, later will switch to eventID
		query = PhaseObf.select().where(\
					PhaseObf.name==self.name)
		if query.exists():
			query = PhaseObf.select().where(\
					PhaseObf.name==self.name).order_by(PhaseObf.phaseID)
		for ix in query:
			phase_obj =  model_to_dict(ix)
			del phase_obj['tableid'], phase_obj['name'] # Delete table id since it's not needed
			## For now we will delete eventID but plan for it in the future
			del phase_obj['eventID']
			phase_obj['other'] = json.loads(phase_obj['other'])
			phaseslist.append(phase_obj)
		return phaseslist

		return phase_obj
	def exportphasejsonstring(self):
		"""Export Player info into a json string

		:param none:
		:type: str
		:return: str
		"""
		phase_obj = self.exportphase()
		return json.dumps(str({'Phase':phase_obj}))
