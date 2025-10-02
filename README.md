
# OBFSQL

A way to convert [Open Bracket Format](https://github.com/openbracketformat/openbracketformat) to SQL and vice versa.

## About Open Bracket Format

A means of interoperability and portability, this format is the standard for an open standard for tournament bracket data.

## The problem 
No real problems with the format itself which is great. However, if you need relational structure, NOSQL makes it a bit difficult (UNIONS and JOINS for example). Thus the motivation for this package.

## The Solution
OBFSQL. It will import and export brackets to SQL (PostgresSQL, MYSQL, and SQLite)






## Installation

Install OBFSQL with pip

```bash
  pip install obfsql
```

### Dependencies 
    "peewee >= 3.15.3",
    "pymysql >= 1.1.1",
    "psycopg>=3.2",
    "psycopg[pool]>=3.2" (This is done to assert pooled connections)
    
## Demo

Let's say you have a bracket named bracket_is_cool.obf

    # Import the main function
    from obfsql import Bracket
    import json
    bracket = Bracket()
    # Connect the database
    bracket.connect(dbtype='sqlite', path='/your/path/here',database='obfsql.db')
    # Create the databse if you haven't done so
    bracket.create_tables()
    # Open the bracket
    with open('/your/path/here/tekken-sunday.obf',          'r') as file:
        data = json.load(file)

    bracket.store(data)


## Roadmap

- Create a Character specific access point
- Make errors/failures/completions more clear


## License

Copyright 2025 Adeboye A Adejare Jr.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
## FAQ

#### Will you be updating this work?

Sparingly. I need motivation to do it, but will do what I can when I can.

#### Can anyone contribute?

Yes. Documentation, demos, or new features would be great.

#### Have you properly tested it.

No.







## Acknowledgements

 - [Open Bracket Format](https://github.com/openbracketformat/openbracketformat) and the community
 - [Read me via Katherine Oelsner](https://readme.so/editor)
 - You, the users.

