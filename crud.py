from model import db, connect_to_db, User, Friend_type, Friend, Social_type, Social_media, Event_type, Event

def create_user(email, password):
    """Create and return a new user"""
    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_friend_type(friend_key, name):
    """create and return a friend type"""
    friend_type = Friend_type(friend_key=friend_key, name=name)

    db.session.add(friend_type)
    db.session.commit()

    return friend_type

def create_friend(user, ftype, full_name, bday, date_met=None, picture=None, 
                  likes=None, dislikes=None):
    """create and return a friend"""

    friend = Friend(user=user, ftype=ftype, full_name=full_name, bday=bday,
                  date_met=date_met, picture=picture, likes=likes, dislikes=dislikes)

    db.session.add(friend)
    db.session.commit()

    return friend

def create_social_type(social_type, name):
    social = Social_type(social_type=social_type, name=name)

    db.session.add(social)
    db.session.commit()

    return account

def create_social_account(friend, stype, url):
    account = Social_media(friend=friend, stype=stype, url=url)

    db.session.add(account)
    db.session.commit()

    return account

if __name__ == '__main__':
    from flask import Flask

    connect_to_db(Flask(__name__))