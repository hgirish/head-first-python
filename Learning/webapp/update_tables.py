import os
import DBcm

db_details = "CoachDB.sqlite3"
FOLDER = "swimdata/"

files = os.listdir(FOLDER)
if ".DS_Store" in files:
  files.remove(".DS_Store")

SQL_SELECT_SWIMMERS  = """
select * from swimmers
where name = ? and age = ?
"""

SQL_INSERT_SWIMMERS = """
insert into swimmers
(name, age)
values
(?, ?)
"""
SQL_SELECT_EVENTS  = """
select * from events
where distance = ? and stroke = ?
"""

SQL_INSERT_EVENTS = """
insert into events
(distance, stroke)
values
(?, ?)
"""

SQL_GET_SWIMMER = """
select id from swimmers
where name = ? and age = ?
"""

SQL_GET_EVENT = """
select id from events
where distance = ? and stroke = ?
"""

SQL_INSERT_TIMES = """
insert into times
(swimmer_id, event_id, time)
values
(?, ?, ?)
"""

with DBcm.UseDatabase(db_details) as db:
    for file in files:
        name, age, distance, stroke = file.removesuffix(".txt").split("-")
        db.execute(SQL_SELECT_SWIMMERS, (name, age))
        if not db.fetchall():
          db.execute(SQL_INSERT_SWIMMERS, (name, age))

        db.execute(SQL_SELECT_EVENTS, (distance, stroke))
        if not db.fetchall():
           db.execute(SQL_INSERT_EVENTS, (distance, stroke))

        db.execute(SQL_GET_SWIMMER, (name,age))
        s_id = db.fetchone()[0]

        db.execute(SQL_GET_EVENT, (distance, stroke))
        e_id = db.fetchone()[0]

        with open(FOLDER + file) as sf:
           times = sf.read().strip().splite(",")
           for t in times:
              db.execute(SQL_INSERT_TIMES, (s_id, e_id, t,))

with DBcm.UseDatabase(db_details) as db:
    db.execute("select * from swimmers")
    results = db.fetchall()
