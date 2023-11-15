from flask import Flask, render_template, session, request
import os
import swimclub
import data_utils
import convert_utils

app = Flask(__name__)
app.secret_key = "You will never guess..."

SELECT_HTML_TEMPLATE = "select.html"


@app.get("/")
def index():
    return render_template("index.html", title="Welcome to SwimClub")


@app.get("/swims")
def display_swim_sesions():
    data = data_utils.get_swim_sessions()
    # =# dates = [session[0].split(" ")[0] for session in data] # SQLite3.
    dates = [str(session[0].date()) for session in data]  # MySQL/MariaDB.

    return render_template(
        "swims.html",
        title="Select a swim session",
        url="/swimmers",
        select_id="chosen_date",
        data=dates,
    )


@app.post("/swimmers")
def display_swimmers():
    session["chosen_date"] = request.form["chosen_date"]
    data = data_utils.get_session_swimmers(session["chosen_date"])
    swimmers = [f"{session[0]}-{session[1]}" for session in data]
    return render_template(
        SELECT_HTML_TEMPLATE,
        title="Select a Swimmer",
        select_id="swimmer",
        url="/showevents",
        data=sorted(swimmers),
    )
@app.post("/swimmersjson")
def json_swimmers():
    session["chosen_date"] = request.json["chosen_date"]
    print( session["chosen_date"])
    data = data_utils.get_session_swimmers(session["chosen_date"])
    swimmers = [f"{session[0]}-{session[1]}" for session in data]
    print(swimmers)
    return swimmers


@app.post("/showevents")
def display_swimmer_events():
    session["swimmer"], session["age"] = request.form["swimmer"].split("-")

    data = data_utils.get_swimmers_events(
        session["swimmer"], session["age"], session["chosen_date"])

    events = [f"{event[0]} {event[1]}" for event in data]

    return render_template(SELECT_HTML_TEMPLATE,
                           url="/showbarchart",
                           title="select an event",
                           select_id="event",
                           data=events,
                           )
@app.post("/eventsjson")
def json_swimmer_events():
    session["swimmer"], session["age"] = request.json["swimmer"].split("-")

    data = data_utils.get_swimmers_events(
        session["swimmer"], session["age"], session["chosen_date"])

    events = [f"{event[0]} {event[1]}" for event in data]
    return events

@app.post("/showbarchart")
def show_bar_chart():
    distance, stroke = request.form["event"].split(" ")

    data = data_utils.get_swimmers_times(
        session["swimmer"],
        session["age"],
        distance,
        stroke,
        session["chosen_date"]
    )

    times = [time[0] for time in data]

    world_records = convert_utils.get_wolrds(distance, stroke)
    average_str, times_reversed, scaled = convert_utils.perform_conversions(
        times)

    header = f"{session['swimmer']} (Under {session['age']}) {distance} {
        stroke} - {session['chosen_date']}"

    return render_template("chart.html",
                           title=header,
                           data=list(zip(times_reversed, scaled)),
                           average=average_str,
                           worlds=world_records)


@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])


def populate_data():
    if "swimmers" in session:
        return
    swim_files = os.listdir(swimclub.FOLDER)
    if ".DS_Store" in swim_files:
        swim_files.remove(".DS_Store")
    session["swimmers"] = {}
    for file in swim_files:
        name, *_ = swimclub.read_swim_data(file)
        if name not in session["swimmers"]:
            session["swimmers"][name] = []
        session["swimmers"][name].append(file)


if __name__ == "__main__":
    app.run(debug=True)
