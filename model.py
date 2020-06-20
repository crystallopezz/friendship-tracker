from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = app = Flask(__name__)

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///friendshiptracker', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String,
                      nullable=False)
    password = db.Column(db.String,
                        nullable=False)

    #friends = list of friend objects that the user has

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Friend_type(db.Model):
    __tablename__ = 'friend_types'

    friend_key = db.Column(db.String,
                         primary_key=True,
                         nullable=False)
    name = db.Column(db.String,
                     nullable=False)

    #friends = list of friend objects with that friend type

    def __repr__(self):
        return f'<Friend_type friend_key={self.friend_key} name={self.name}>'

class Friend(db.Model):
    __tablename__ = 'friends'

    friend_id = db.Column(db.Integer,
                        primary_key=True, 
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    full_name = db.Column(db.String,
                          nullable=False)
    bday = db.Column(db.DateTime,
                     nullable=False)
    date_met = db.Column(db.DateTime)
    picture = db.Column(db.String)
    friend_type = db.Column(db.String,
                            db.ForeignKey('friend_types.friend_key'))
    likes = db.Column(db.Text)
    dislikes = db.Column(db.Text)

    user = db.relationship('User', backref='friends')
    ftype = db.relationship('Friend_type', backref='friends')

    #social_medias = list of social media accounts friend has
    #events = list of events this friend has

    def __repr__(self):
        return f'<Friend friend_id={self.friend_id} name={self.full_name}>'


class Social_type(db.Model):
    __tablename__ = 'social_types'

    social_type = db.Column(db.String,
                            primary_key=True)
    name = db.Column(db.String,
                     nullable=False)

    #social_medias = list of social_media accts w/ this social_type

    def __repr__(self):
        return f'<Social_type social_type={self.social_type} name={self.name}>'

class Social_media(db.Model):
    __tablename__ = 'social_medias'

    social_id = db.Column(db.Integer,
                        primary_key=True, 
                        autoincrement=True)
    friend_id = db.Column(db.Integer,
                          db.ForeignKey('friends.friend_id'), 
                          nullable=False)
    social_type = db.Column(db.String, 
                            db.ForeignKey('social_types.social_type'))
    url = db.Column(db.String,
                    nullable=False)

    friend = db.relationship('Friend', backref='social_medias')
    stype = db.relationship('Social_type', backref='social_medias')

    def __repr__(self):
        return f'<Social_media social_id={self.social_id} type={self.social_type}>'

class Event_type(db.Model):
    __tablename__ = 'event_types'

    event_key = db.Column(db.String,
                          primary_key=True)
    event_type = db.Column(db.String,
                           nullable=False)

    #events = list of events with this event_key

    def __repr__(self):
        return f'<Event_type event_type={self.event_type}>'

class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    friend_id = db.Column(db.Integer,
                          db.ForeignKey('friends.friend_id'),
                          nullable=False)
    event_type = db.Column(db.String,
                           db.ForeignKey('event_types.event_key'),
                           nullable=False)
    details = db.Column(db.Text)
    date = db.Column(db.DateTime,
                     nullable=False)

    friend = db.relationship('Friend', backref='events')
    etype = db.relationship('Event_type', backref='events')

    def __repr__(self):
      return f'<Event event_id={self.event_id}>'

if __name__ == '__main__':

    connect_to_db(app)