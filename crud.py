from model import db, connect_to_db, User, Friend_type, Friend, Social_type, Social_media, Event_type, Event

def create_user(email, password):
    """Create and return a new user"""
    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

if __name__ == '__main__':
    from flask import Flask

    connect_to_db(Flask(__name__))