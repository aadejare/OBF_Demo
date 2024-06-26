#! /usr/bin/
import re, os, sys, time, shutil, numpy, json
import pycountry, python_jsonschema_objects as pjs

schema = {
    "$schema": "http://json-schema.org/draft-06/schema",
    "$ref": "#/definitions/Tournament",
    "definitions": {
        "Tournament": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event": {
                    "$ref": "#/definitions/Event",
                    "description": "Object that contains metadata relevant to the entire tournament -- e.g. name and date of the event, tournament format, etc. See the `Event` definition for more information."
                },
                "sets": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Set"
                    },
                    "description": "Unordered array of all sets that took place during this tournament. See the `Set` definition for more information."
                },
                "entrants": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Entrant"
                    },
                    "description": "Unordered array of all entrants in the tournament. See the `Entrant` definition for more information."
                },
                "version": {
                    "type": "string",
                    "enum": ["v0.1", "v0.2"],
                    "description": "Stores the version of the Open Bracket Format specification that this file was generated in accordance with. It is highly recommended (but not required) to include this field -- if this field is not set, the default assumption will be that the file was generated with the most recent version of OBF. The current version of the OBF format (what you are reading) is `v0.2`."
                }
            },
            "required": ["event", "sets", "entrants"],
            "title": "Tournament",
            "description": "Root object: every OpenBracketFormat file should consist of exactly one `Tournament` object."
        },
        "Event": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "description": "String containing the title of this event. This is a required field."
                },
                "date": {
                    "type": "string",
                    "format": "date",
                    "description": "Start date of the event. Should be provided in ISO 8601 format (YYYY-MM-DD)."
                },
                "gameName": {
                    "type": "string",
                    "description": "String representing the name of the game played at this event."
                },
                "tournamentStructure": {
                    "type": "string",
                    "description": "String representing the format of this tournament (e.g. single-elimination, double-elimination, etc.). This field should only be used to record format as it relates to the structure of the tournament (i.e. how matches are decided) and not format as it pertains to game-specific factors (e.g. whether it's a teams tournament, the ruleset in use, etc.). For commonly-used structures, use the following identifiers: 'single-elim' (Single elimination), 'double-elim' (Double elimination), 'round-robin' (Round robin)."
                },
                "phases": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Phase"
                    },
                    "description": "Array of `Phase` objects containing information about each phase of this tournament. Useful for capturing complicated tournament structures, like round-robin pools leading into a double-elimination bracket (where different phases may have different structures). See the `Phase` definition for more information."
                },
                "ruleset": {
                    "type": "string",
                    "description": "String representing the choice of ruleset."
                },
                "originURL": {
                    "type": "string",
                    "description": "String containing a external URL linking to the original source of this data (e.g. an external tournament website)."
                },
                "numberEntrants": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Integer containing the number of entrants in this tournament. If populated, this should be equal to the length of the `entrants` subarray of the root `Tournament` object."
                },
                "other": {
                    "type": "object",
                    "description": "Object that can be used to store any other relevant event-related information not covered by the previously mentioned fields."
                }
            },
            "required": ["name"],
            "title": "Event",
            "description": "Object containing metadata relevant to the entire event, such as the name and date of the event, game played, the format of the tournament (e.g. whether it was single-elim or double-elim), etc."
        },
        "Entrant": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "entrantID": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Unique string ID corresponding to this entrant. This ID can be an autogenerated identifier, some form of the player's tag, or the player's tag itself, as long as it is guaranteed that no two different entrants share the same `entrantID`. Entrants in `Set` objects are referenced by this ID. This is a required field."
                },
               "entrantTeam": {
                    "type": "boolean",
                    "enum": [False, True],
                    "description": "Field to identify if entrant is a part of a multi-entrant team. Default is False."
                },
                "entrantTag": {
                    "type": "string",
                    "description": "String containing the entrant's ``tag; in other words, the name the entrant chooses when registering for the tournament, that appears in results, etc."
                },
                "initialSeed": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Integer representing the initial seeding of this entrant. Larger seeds are worse seeds; 1 is the best possible seed."
                },
                "finalPlacement": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Integer representing the final placing of this entrant."
                },
                "personalInformation": {
                    "$ref": "#/definitions/PersonalInformation",
                    "description": "Object containing personal data about this entrant (e.g. legal name, country, etc.)."
                },
                "other": {
                    "type": "object",
                    "description": "Object that can be used to store any other relevant entrant-related information not covered by the previously mentioned fields."
                }
            },
            "required": ["entrantID"],
            "title": "Entrant",
            "description": "Object representing an entrant in the tournament. Every unique entrant which appears in a set should have a corresponding `Entrant` object in the `entrants` subfield of `Tournament`."
        },
        "PersonalInformation": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {
                    "type": "string",
                    "description": "String containing entrant's legal name."
                },
                "country": {
                    "type": "string",
                    "description": "String containing entrant's country."
                },
                "other": {
                    "type": "object",
                    "description": "Object that can be used to store any other relevant personal entrant-related information not covered by the previously mentioned fields."
                },
                "gender": {
                    "type": "string",
                    "description": "String containing entrant's gender."
                },
                "pronouns": {
                    "type": "string",
                    "description": "String containing entrant's pronouns for identification"
                },
                "language": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "An array of string containing entrant's language to communicate from most to least frequently used."
                },
            },
            "required": [],
            "title": "PersonalInformation",
            "description": "Object representing personal information (e.g. name, country) associated with an entrant. Subobject of `Entrant`."
        },
        "Set": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "setID": {
                    "type": "string",
                    "description": "String containing a unique identifier for this set (i.e. no two sets in the event's `sets` array should have the same setID)."
                },
                "entrant1ID": {
                    "type": "string",
                    "description": "The entrantID of the first player in this match."
                },
                "entrant2ID": {
                    "type": "string",
                    "description": "The entrantID of the second player in this match."
                },
                "status": {
                    "type": "string",
                    "enum": ["completed", "started", "pending"],
                    "description": "String representing the status of this set. If populated, must take one of the following values: 'completed' (if the set has finished), 'started' (if the set is currently in progress), or 'pending' (if the set has yet to start)."
                },
                "entrant1Result": {
                    "type": "string",
                    "enum": ["win", "lose", "draw"],
                    "description": "String representing the result of entrant 1 in this match. If populated, must equal either 'win', 'lose', or 'draw'."
                },
                "entrant2Result": {
                    "type": "string",
                    "enum": ["win", "lose", "draw"],
                    "description": "String representing the result of entrant 2 in this match. If populated, must equal either 'win', 'lose', or 'draw'."
                },
                "entrant1Score": {
                    "type": "integer",
                    "description": "Integer representing the score of entrant 1 in this match."
                },
                "entrant2Score": {
                    "type": "integer",
                    "description": "Integer representing the score of entrant 2 in this match."
                },
                "winnerNextSetID": {
                    "type": "string",
                    "description": "The setID of the set that the winner of this set will play next. For a single-elim or double-elim tournament, setting this allows one for reconstruction of the original bracket. If the winner of this set does not play another set (e.g. in the case of finals), do not set this field."
                },
                "loserNextSetID": {
                    "type": "string",
                    "description": "The setID of the set that the loser of this set will play next. For a double-elim tournament, setting this allows one for reconstruction of the original bracket. If the loser of this set does not play another set (e.g. in the case of finals or a match in the losers side of the bracket), do not set this field."
                },
                "entrant1PrevSetID": {
                    "type": "string",
                    "description": "The setID of the set that entrant 1 played right before this set. If this is entrant 1's first set, do not set this field."
                },
                "entrant2PrevSetID": {
                    "type": "string",
                    "description": "The setID of the set that entrant 2 played right before this set. If this is entrant 2's first set, do not set this field."
                },
                "setFormat": {
                    "type": "string",
                    "description": "String representing format specific to this set (e.g. whether it was best of 3 or best of 5)."
                },
                "phaseID": {
                    "type": "string",
                    "description": "String representing the `phase' of this specific set. It is up to the user's discretion to decide what precisely a phase means. For tournaments with multiple phases / levels (e.g. pools, top 64, top 8), it is convenient to record this information here."
                },
                "roundID": {
                    "type": "string",
                    "description": "String representing the `round' in the bracket of this specific set (for example, \"Winner's Round 1\" or \"Semifinals\"). It is up to the user's discretion to decide what precisely a round means and how to record it."
                },
                "games": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Game"
                    },
                    "description": "Array of `Game` objects containing information about each game of this set. It is recommended (but not required) that this array records the games in chronological order. See the `Game` definition for more information."
                },
                "other": {
                    "type": "object",
                    "description": "Object that can be used to store any other relevant set-related information not covered by the previously mentioned fields."
                }
            },
            "required": ["setID"],
            "title": "Set",
            "description": "Object representing a single set of the tournament."
        },
        "Game": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "gameNumber": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Integer representing the number (in chronological order) of this game. The `gameNumber`s of the games of a set should be unique and span a consecutive range of integers starting at 1."
                },
                "entrant1Characters": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Array of strings representing the character(s) played by entrant 1 in this game. If entrant 1 only plays a single character in this game (most cases), this field should contain an array containing a single string (entrant 1's character). In team games or games where each entrant can choose a selection of different characters, you should record these characters as separate elements of this field."
                },
                "entrant2Characters": {
                    "type": "array",
                    "description": "Array of strings representing the character(s) played by entrant 2 in this game. See also `entrant1Characters`."
                },
                "stage": {
                    "type": "string",
                    "description": "String representing the stage this game was played on."
                },
                "entrant1Result": {
                    "type": "string",
                    "enum": ["win", "lose", "draw"],
                    "description": "String representing the result of entrant 1."
                },
                "entrant2Result": {
                    "type": "string",
                    "enum": ["win", "lose", "draw"],
                    "description": "String representing the result of entrant 2."
                },
                "other": {
                    "type": "object",
                    "description": "Object that can be used to store any other relevant game-related information not covered by the previously mentioned fields."
                }
            },
            "required": ["gameNumber"],
            "title": "Game",
            "description": "Object representing a single game of a set."
        },
        "Phase": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "phaseID": {
                    "type": "string",
                    "description": "Unique string ID corresponding to this phase."
                },
                "phaseStructure": {
                    "type": "string",
                    "description": "String representing the format of this tournament in this phase (e.g. single-elimination, double-elimination, etc.). See the `tournamentStructure` field in `Event` for more information."
                },
                "other": {
                    "type": "object",
                    "description": "Object that can be used to store any other relevant phase-related information not covered by the previously mentioned fields."
                }
            },
            "required": ["phaseID"],
            "title": "Phase",
            "description": "Object representing a single phase of a tournament (e.g. pools, top 64, etc.) Useful for recording tournaments with complex structures (e.g. round-robin pools into a double-elimination bracket). See the `phases` field in `Event` for more information."
        }
    }
}

import warnings

## python_jsonschema_objects currently does not support  with Draft 6 Schema which is used for OBS (April 15, 2024)
## Function embedded with warnings
def PersonalInformation():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		builder = pjs.ObjectBuilder(schema)
		class_builder = builder.build_classes()
		obs_class=class_builder.Personalinformation
		return obs_class
def Tournament():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		builder = pjs.ObjectBuilder(schema)
		class_builder = builder.build_classes()
		obs_class=class_builder.Tournament
		return obs_class
def TournamentEvent():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		builder = pjs.ObjectBuilder(schema)
		class_builder = builder.build_classes()
		obs_class=class_builder.Tournament
		return obs_class	
def TournamentSet():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		builder = pjs.ObjectBuilder(schema)
		class_builder = builder.build_classes()
		obs_class=class_builder.Set
	return obs_class
def TournamentPhase():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		builder = pjs.ObjectBuilder(schema)
		class_builder = builder.build_classes()
		obs_class=class_builder.Phase
		return obs_class	
def TournamentGame():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		builder = pjs.ObjectBuilder(schema)
		class_builder = builder.build_classes()
		obs_class=class_builder.Game
		return obs_class
# country = pycountry.countries.search_fuzzy('America')
# language = pycountry.languages.get(name='English').alpha_2

# Player = PI(name='test', country='United States of America',gender='Male',pronouns='he/him',language='en')
# print((Player))
# player['name'] = 'Test'
# player['country'] = country[1].name
# player['gender'] = 'Male'
# player['pronouns'] = 'He/him'
# player['language'] = language

# Player = Personalinformation(name='test', country=country[1].name,gender='Male',pronouns='he/him',language=language)

