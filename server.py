from flask import Flask, render_template
import os
import sys

SECRET_KEY = os.environ.get('APP_KEY', 'FOR_LOOP')


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/about/")
def about_us():
    return render_template('about_us.html')


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True
    else:
        app.debug = False

    app.run()