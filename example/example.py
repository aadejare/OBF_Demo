#!/usr/bin/env python
import re, os, sys, time, shutil, json

#Import OBFmodel

import Event, MatchSet, Entrant, Game, Phase, Tournament

data = None
with open('example.json', 'r') as file:
	data = json.load(file)

print("Tournament Data: \n\n")
tourn_data = Tournament.Tournament(tournamentTitle='First Tourney', obfversion='1.0',
			description='My first tourney!', definitions= {
    "SetGameResult": {
      "enum": [ "win", "lose", "draw", "dq" ]
    } }, tournamentID='60a4345c2fccc4a1fcd5a0fa2b241f4c')
print (tourn_data.tournamentID)
print(tourn_data.savetournament())
print('Now new')
print(tourn_data.savetournament('update'))
print (tourn_data.tournamentID)
print(tourn_data.exporttournamentjson())
print(data)
	
	
print ('Next Phase Data: \n\n')
phase_data = Phase.Phase( phaseID= 'fd1a7398c11d729cc9dc3fbe67342700',
						phaseStructure='Final')
phase_data.savephase(savedata='new')	

				
print("Event data:  \n\n")
event_obf = data['event']

event_data = Event.Event(eventDate=event_obf['date'], gameName=event_obf['gameName'],\
					ruleset=event_obf['ruleset'],originURL=event_obf['originURL'],\
					name=event_obf['name'], numberEntrants = event_obf['numberEntrants'],
					tournamentStructure= event_obf['tournamentStructure'],
					tournamentID= tourn_data.tournamentID,
					phaseID = phase_data.phaseID)
event_data.saveeventinfo('new')

print('Set data: \n\n')
for i in range(0, len(data['sets'])):
	set_data_parse = data['sets'][i]
	set_data = MatchSet.MatchSet(entrant1ID=set_data_parse['entrant1ID'],\
			entrant2ID=set_data_parse['entrant2ID'], status=set_data_parse['status'], \
			entrant1Result=set_data_parse['entrant1Result'], \
			entrant2Result=set_data_parse['entrant2Result'],\
			entrant1Score=set_data_parse['entrant1Score'], \
			entrant2Score=set_data_parse['entrant2Score'],\
			entrant1NextSetID=set_data_parse['entrant1NextSetID'], \
			entrant2NextSetID=set_data_parse['entrant2NextSetID'],\
			setFormat=set_data_parse['setFormat'], \
			phaseID=phase_data.phaseID,
			setID =set_data_parse['setID'],
			tournamentID=tourn_data.tournamentID)
	set_data.saveset('new')
	print("THIS IS SET ID: " + str(set_data.setID))
	game_data_set = set_data_parse['games']
	print ('Game data: \n\n\n')
	for jx in game_data_set:
		game_data_parse = jx
		game_data = Game.Game(gameNumber=game_data_parse['gameNumber'], 
		entrant1Characters=game_data_parse['entrant1Characters'],\
		entrant2Characters=game_data_parse['entrant2Characters'],\
			stage=game_data_parse['stage'], \
			entrant1Result=game_data_parse['entrant1Result'],\
			 entrant2Result=game_data_parse['entrant2Result'],\
			 setID=set_data.setID,\
				other=None)
		game_data.savegame('new')
# 	print(set_data.exportset())
print ('Entrant data: \n\n\n')
print(data['entrants'])
for i in range(0, len(data['entrants'])):
	entrant_parse = data['entrants'][i]
	print (entrant_parse['entrantTag'],)
	entrant_Data = Entrant.Entrant(entrantID = entrant_parse['entrantTag'], 
							entrantTag = entrant_parse['entrantTag'], 
					finalPlacement=entrant_parse['finalPlacement'], 
					initialSeed=entrant_parse['initialSeed'], 
					personalInformation =entrant_parse['personalInformation'],
					tournamentID = tourn_data.tournamentID )
	print(entrant_Data.entrantTag)
	entrant_Data.saveentrantinfo('update')
# 	print(entrant_Data.exportentrants())
# 	