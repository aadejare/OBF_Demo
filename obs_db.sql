-- TABLE
CREATE TABLE EntrantOBF (
  tableid Text NOT NULL PRIMARY KEY,
  setID text NOT NULL UNIQUE,
  entrantTag text,
  initialSeed integer,
  finalPlacement integer,
personalInformation text unique,
  pronouns text,
  language blob,
  other blob
  );
CREATE TABLE EventOBF (
  tableid Text NOT NULL PRIMARY KEY,
  name text NOT NULL,
  eventDate text,
  gameName text,
tournamentStructure text,
  phases blob,
    ruleset text,
  originURL text,
  numberEntrants integer,
  other blob,
 phaseID text UNIQUE  
  );
CREATE TABLE GameOBF (
tableid Text NOT NULL PRIMARY KEY,
gameNumber integer NOT NULL UNIQUE,
entrant1Characters blob,
entrant2Characters blob,
stage text,
entrant1Result text CHECK (entrant1Result in ('win','lose','draw','Win','Lose','Draw','WIN','LOSE','DRAW')),
entrant2Result text CHECK (entrant2Result in ('win','lose','draw','Win','Lose','Draw','WIN','LOSE','DRAW')),
other blob
);

CREATE TABLE CharactersObf  (
  tableid integer NOT NULL PRIMARY KEY,
  entrantCharacterName TEXT,
  entrantCharacterNameID TEXT NOT NULL
);

CREATE TABLE PersonalInformationOBF (
  tableid Text NOT NULL PRIMARY KEY,
  name text,
  country text,
  gender text,
  pronouns text,
  language blob,
  entrant_tag text NOT NULL UNIQUE,
  other blob  );
CREATE TABLE PhaseOBF (
  tableid Text NOT NULL PRIMARY KEY,
  phaseID text NOT NULL UNIQUE,
  phaseStructure text,
  other blob
  );
CREATE TABLE TournamentOBF (
  tableid Text NOT NULL PRIMARY KEY,
  event text NOT NULL,
  sets blob NOT NULL,
  entrants blob NOT NULL,
obfversion text,
 CHECK (obfversion in ('v0.1', 'v0.2','1.0'))
  );
 
-- INDEX
 
-- TRIGGER
 
-- VIEW
 
