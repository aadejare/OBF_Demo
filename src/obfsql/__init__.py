# Define the __all__variable

import os, sys
sys.path.insert(0, os.path.abspath(__file__))

__all__ = ["Bracket",'Entrant','Event','Game','MatchSet',\
			'PersonalInformation', 'Phase', 'Tournament']

version = 0.1

# from .Bracket import Bracket