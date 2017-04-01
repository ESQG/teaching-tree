from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class NaturalLanguage(db.Model):
    __tablename__ = "natural_languages"
    language_code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    i_speak_this_language = db.Column(db.String(500))

class Medium(db.Model):
    __tablename__ = "media"
    medium_code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    

class Subject(db.Model):
    __tablename__ = "subjects"
    subject_code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)


class AccessNeeds(db.Model):
    __tablename__ = "access_needs"
    an_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_type = db.Column(db.String(100))
    acccomodations = db.Column(db.Text)



class ComputerLanguage(db.Model):
    __tablename__ = "computer_languages"

    language_code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    characteristics = db.Column(db.Text)


class Resource(db.Model):
    __tablename__ = "resources"

    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    url = db.Column(db.Text)
    # medium = db.Column(db.String(10), db.ForeignKey('media.medium_code'))
    medium = db.Column(db.String(20))
    natural_language = db.Column(db.String(20), db.ForeignKey('natural_languages.language_code'))
    computer_language = db.Column(db.String(20), db.ForeignKey('computer_languages.language_code'))
    subject = db.Column(db.String(20), db.ForeignKey('subjects.subject_code'))
    audience = db.Column(db.String(20), db.ForeignKey('audiences.audience_code'))
    notes = db.Column(db.Text)

class Audience(db.Model):
    __tablename__ = "audiences"

    audience_code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    rank = db.Column(db.Integer, unique=True)
    notes = db.Column(db.Text)

class User(db.Model):
    __tablename__ = "users"
 
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    natural_language = db.Column(db.String(20), db.ForeignKey('natural_languages.language_code'))
    computer_language = db.Column(db.String(20), db.ForeignKey('computer_languages.language_code'))
    subject = db.Column(db.String(20), db.ForeignKey('subjects.subject_code'))
    audience = db.Column(db.String(20), db.ForeignKey('audiences.audience_code'))


class UserNeeds(db.Model):
    """Association table for users and access needs."""

    __tablename__ = "user_needs"

    un_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    access_need_id = db.Column(db.Integer, db.ForeignKey('access_needs.an_id'))


def connect_to_db(app, db_uri='postgresql:///teaching-tree', echo=False):
    """Connect a Flask app to our database."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)
    print "Connected to db %s" % db_uri.split('/')[-1] # Text after the last '/'


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    db.create_all()     # Creates any tables the model needs that have not been created yet