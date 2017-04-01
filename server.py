from flask import Flask, render_template, redirect, request, jsonify
import os
import sys
import json

SECRET_KEY = os.environ.get('APP_KEY', 'FOR_LOOP')


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def home_page():
    data = read_json_data()
    return render_template('index.html', subjects=data['subjects'])

@app.route("/about")
def about_us():
    return render_template('about_us.html')

@app.route("/learn")
def learn():
    subject = request.args.get('subject').strip().lower()   # Makes it lowercase
    if not subject:
        subject = request.args.get('select-subject')

    data = read_json_data()
    if subject in data['subjects']:
        return render_template('resources.html', subject=subject, resources=data["resources"].get(subject, []))
    else:
        return redirect("/suggest/"+subject)

@app.route("/suggest/<subject>")
def suggest(subject):
    return render_template('new_subject.html', subject=subject)



@app.route("/test.json")
def show_data():
    return jsonify(json.load(open("resources.json")))


def read_json_data():
    try:
        raw_data = json.load(open("resources.json"))
        return raw_data

    except ValueError:
        print ("Could not parse JSON!")
        return {"resources": [], "subjects": []}


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
    else:
        app.debug = False

    app.run()