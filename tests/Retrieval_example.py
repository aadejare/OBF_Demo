#!/usr/bin/env python
"""
Retrieval_example.py
Retrieve all the data in the proper format.
"""
import os, json

#Import OBFmodel
from obfmodels import db
from playhouse.sqlite_ext import SqliteExtDatabase

import Event, MatchSet, Entrant, Game, Phase, Tournament


PROJECT_PATH  = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', ''))
# db_sqlite = SqliteExtDatabase(PROJECT_PATH + '/obfsql.db', regexp_function=True, timeout=3,
#                        pragmas={'journal_mode': 'wal'})

from playhouse.db_url import connect as phconnect

db_sqlite = phconnect('sqlite:///obfsql.db')
db.initialize(db_sqlite)
OBF = None 
#Get Tournament data
tourn_ex = Tournament.Tournament(tournamentTitle='Tournament new quick')
tourn_ex.gettournamentID()
print(tourn_ex.tournamentID)
# OBF = tourn_ex.exporttournament()
# print (OBF)
# # Get event data
# event_ex = Event.Event(name="Example Tournament", tournamentID=tourn_ex.tournamentID)
# event_ex2 = event_ex.exportevent()
# del event_ex2['tournamentID']
# print(event_ex2)
# OBF['event'] = event_ex2
# phase_data = Phase.Phase( phaseID= 'fd1a7398c11d729cc9dc3fbe67342700', name=event_ex.name)
# OBF['phases'] = phase_data.exportphases()
# print(event_ex2)
# 
# set_ex = MatchSet.MatchSet(setID='1',
# 			tournamentID=tourn_ex.tournamentID)
# set_ex.getset()
# set_ex2 = set_ex.exportset()
# game_ex=Game.Game(setID=set_ex.setID)
# set_ex2['games'] = game_ex.exportgames()
# print('\n\n\n\nNew set print: \n\n\n')
# print(event_ex2)
# OBF['sets'] = [set_ex2]
# entrant_ex = Entrant.Entrant(tournamentID = tourn_ex.tournamentID )
# OBF['entrants'] = entrant_ex.exportentrants()
# print('\n\n\n\nNew set print final bracket: \n\n\n')
# OBF['event'] = event_ex2
# print(json.dumps(OBF, indent=4))
