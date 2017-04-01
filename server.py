from flask import Flask, render_template, redirect, request, jsonify, flash
import os
import sys
import json

import data_interface
from model import connect_to_db

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

    if not subject:
        flash("Had an error: please pick a subject.")
        return redirect("/")

    known_subject = data_interface.get_subject(subject)
    if not known_subject:
        return render_template("new_subject.html", subject=subject)

    subject_code = known_subject.subject_code
    resources = data_interface.get_resources(subject_code)
    return render_template("resources.html", resources=resources, subject=subject)

@app.route("/suggest/<subject>")
def suggest(subject):
    languages = data_interface.get_languages()
    audiences = data_interface.get_audiences()
    resources = data_interface.get_resources(subject)
    return render_template('new_subject.html', subject=subject, audiences=audiences, languages=languages)


@app.route("/add-resource", methods=["POST"])
def add_new_resource():
    subject = request.form.get("subject")
    resource_data = {
    "subject": subject,
    "reading-level": int(request.form.get("reading-level")),
    "subject-detail": request.form.get("subject-detail"),
    "notes": request.form.get("notes"),
    "url": request.form.get("link"),
    "language": request.form.get("language"),
    "medium": request.form.get("medium"),
    "title": request.form.get("title")
    }

    with open("form_submission.log", 'w') as outfile:
        outfile.write(str(resource_data))

    data_interface.add_resource(resource_data)
    flash("Thank you for providing this resource in %s!" % subject)
    return redirect("/")

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
    connect_to_db(app)

    app.run()
