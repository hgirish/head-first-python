from flask import Flask, render_template, session
import os
import swimclub


app = Flask(__name__)
app.secret_key = "You will never guess..."


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/swimmers")
def display_swimmers():
    populate_data()
    return str(sorted(session["swimmers"]))

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
