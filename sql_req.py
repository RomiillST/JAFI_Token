import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS Users (
TG_ID INT,
NAME STR,
BALANCE INT,
TOTAL INT,
STAGE INT
)
''')

first_insert = '''
INSERT INTO Users(TG_ID, BALANCE, TOTAL, STAGE) VALUES ('{}',0, 0, 0)
'''
admin_insert = '''
INSERT INTO Users VALUES ('{}', 'Director', 0, 0, 50)
'''

set_name = '''
UPDATE Users
SET NAME = '{}'
WHERE TG_ID = '{}'
'''

set_balance = '''
UPDATE Users
SET BALANCE = '{}'
WHERE TG_ID = '{}'
'''

set_stage = '''
UPDATE Users
SET STAGE = '{}'
WHERE TG_ID = '{}'
'''

select_id = '''
SELECT TG_ID
FROM Users
WHERE TG_ID = '{}'
'''

select_all_ids = '''
SELECT TG_ID
FROM Users
WHERE TG_ID > 0
'''

select_name = '''
SELECT NAME
FROM Users
WHERE TG_ID = '{}'
'''

select_balance = '''
SELECT BALANCE
FROM Users
WHERE TG_ID = '{}'
'''

select_stage = '''
SELECT STAGE
FROM Users
WHERE TG_ID = '{}'
'''

set_total = '''
UPDATE Users
SET TOTAL = '{}'
WHERE TG_ID = '{}'
'''

select_total = '''
SELECT TOTAL
FROM Users
WHERE TG_ID = '{}'
'''



full_insert = '''
INSERT INTO Users (TG_ID, NAME, TOTAL) VALUES ('{}', '{}', '{}')
'''