-- TABLE
CREATE TABLE EntrantOBF (
  tableid INTEGER PRIMARY KEY,
  setID text NOT NULL UNIQUE,
  entrantTeam BOOLEAN,
  entrantTag text,
  initialSeed integer,
  finalPlacement integer,
personalInformation integer,
  pronouns text,
  language blob,
  other blob
  );
CREATE TABLE EventOBF (
  tableid INTEGER PRIMARY KEY,
  name text NOT NULL,
  eventdate text,
  gameName text,
tournamentStructure text,
  phases blob,
    ruleset text,
  originURL text,
  numberEntrants integer,
  other blob,
 phaseID  UNIQUE  
  );
CREATE TABLE GameOBF (
  tableid INTEGER PRIMARY KEY,
  gameNumber integer NOT NULL UNIQUE,
  entrant1Characters text,
  entrant2Characters text,
  stage text,
 entrant1Result text CHECK ( entrant1Result in ('win','lose','draw','Win','Lose','Draw','WIN','LOSE','DRAW')),
  entrant2Result text CHECK (entrant2Result in ('win','lose','draw','Win','Lose','Draw','WIN','LOSE','DRAW')),
  other blob
  );
CREATE TABLE PersonalInformationOBF (
  tableid INTEGER PRIMARY KEY,
  name text,
  country text,
  gender text,
  pronouns text,
  language blob,
  other blob  );
CREATE TABLE PhaseOBF (
  tableid INTEGER PRIMARY KEY,
  phaseID text NOT NULL UNIQUE,
  phaseStructure text,
  other blob
  );
CREATE TABLE TournamentOBF (
  tableid INTEGER PRIMARY KEY,
  event text NOT NULL,
  sets blob NOT NULL,
  entrants blob NOT NULL,
obfversion text,
 CHECK (obfversion in ('v0.1', 'v0.2'))
  );
 
-- INDEX
 
-- TRIGGER
 
-- VIEW
 
