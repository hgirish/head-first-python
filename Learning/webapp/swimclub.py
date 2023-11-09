import statistics
import hfpy_utils
import os
import json

CHARTS = "charts/"
FOLDER = "swimdata/"
JSONDATA = "records.json"


def read_swim_data(filename):
    """Return swim data from a file.
    Given the name of  a swimmer's file (in filename), extract all the required
    data, then return it to the caller as tuple.
    """
    swimmer, age, distance, stroke = filename.removesuffix(".txt").split("-")
    with open(FOLDER + filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(",")

    converts = []
    for t in times:
        # The minutes value might be missing, so guard against this causing a crash.
        if ":" in t:
            minutes, rest = t.split(":")
        else:
            minutes = "0"
            rest = t
        second, hundredths = rest.split(".")
        converts.append((int(minutes)*60*100) +
                        (int(second)*100) + int(hundredths))

    average = statistics.mean(converts)
    mins_secs, hundredths = f"{(average/100):.2f}".split(".")
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs - minutes*60
    average = f"{minutes}:{seconds:0>2}.{hundredths}"
    return swimmer, age, distance, stroke, times, average, converts  # Returned as a tuple


def produce_bar_chart(fn, location=CHARTS):
    """Given the name of swimmer's file, produce a HTML/SVG-based bar chart
     Save the chart to the CHARTS folder. Return the path to the bar chart file.
    """

    swimmer, age, distance, stroke,  times, average, converts = read_swim_data(
        fn)
    from_max = max(converts)

    times.reverse()
    converts.reverse()

    title = f"{swimmer} (Under {age}) {distance} {stroke}"

    header = f"""<!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            <link rel="stylesheet" href="/static/webapp.css" />
        </head>
        <body>
            <h3>{title}</h3>
     """
    body = ""
    for n, t in enumerate(times, 0):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 400)
        body += f"""
    <svg height="30" width="450">
        <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
    </svg>{t}<br />
            """
    with open("records.json") as jf:
        records = json.load(jf)
    COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
    times = []
    for course in COURSES:
        times.append(records[course][event_lookup(fn)])
    footer = f"""
    <p>Average time: {average}</p>
    <p>M: {times[0]} ({times[2]})<br />
    W: {times[1]} ({times[3]})</p>
    </body>
    </html>
    """

    page = header + body + footer

    save_to = f"{location}{fn.removesuffix('.txt')}.html"

    with open(os.path.realpath(save_to), "w") as sf:
        print(page, file=sf)

    return save_to


def event_lookup(event):
    """Convert from filenames to dictionary keys.

    Given an event descriptor (the name of a swimmer's file), convert
    the descriptior into a lookup key which can be used with the "records"
    dictionary.    
    """
    conversions = {
        "Free": "freestyle",
        "Back": "backstroke",
        "Breast": "breaststoke",
        "Fly": "butterfly",
        "IM": "individual medly",
    }
    *_, distance, stroke = event.removesuffix(".txt").split("-")
    return f"{distance} {conversions[stroke]}"
