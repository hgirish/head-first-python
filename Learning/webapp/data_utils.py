from queries import *
import DBcm

# -# db_details = "CoachDB.sqlite3"

db_details = {
    "host": "localhost",
    "database": "swimDB",
    "user": "swimuser",
    "password": "swimpasswd",
}


def get_swim_sessions():
    """Return a tuple-list of unique session timestamps."""
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_SESSIONS)
        results = db.fetchall()
    return results


def get_session_swimmers(date):
    """When given a date (YYYY-MM-DD), return a tuple-list of swimmers
    and their associated age (filtered by date)
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_SWIMMERS_BY_SESSION, (date, ))
        results = db.fetchall()
    return results


def get_swimmers_events(swimmer, age, date):
    """When given a date (YYYY-MM-DD), swimmer's name and swimmer's age, return
    a tuple-list of events the swimmer swam on the date.
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_SWIMMERS_EVENTS_BY_SESSION, (swimmer, age, date,))
        results = db.fetchall()
    return results


def get_swimmers_times(name, age, distance, stroke, date):
    """When given a date (YYYY-MM-DD), swimmer's name, swimmer's age, distance, and stroke,
    return a tuple-list of times the swimmer swam on that date over the identified
    distance/stroke combination.
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
                   (name, age, distance, stroke, date,))
        results = db.fetchall()
    return results
