from model import db, connect_to_db, User, Friend_type, Friend, Social_type, Social_media, Event_type, Event, app

def create_user(email, password):
    """Create and return a new user"""
    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """return user with email"""
    return User.query.filter(User.email==email).first()

def validate_user_password(input_pw, email):
    """check if input password matches user's password"""
    user = get_user_by_email(email)

    #TODO - add check for if a user with that email exists. 

    return user.password == input_pw

def get_user_by_id(user_id):
    user = User.query.get(user_id)
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

def get_friend_by_friend_id(friend_id):
    
    return Friend.query.get(friend_id)

     

def get_friends_by_user_id(user_id): 
    user = User.query.get(user_id)
    friends = user.friends
    return friends

def create_social_type(social_type, name):
    social = Social_type(social_type=social_type, name=name)

    db.session.add(social)
    db.session.commit()

    return social

def create_social_account(friend, stype, url):
    account = Social_media(friend=friend, stype=stype, url=url)

    db.session.add(account)
    db.session.commit()

    return account

def create_event_type(event_key, event_type):
    """create and return an event type"""
    event=Event_type(event_key=event_key, event_type=event_type)

    db.session.add(event)
    db.session.commit()

    return event_type

def create_event(friend, etype, details, date):
    """create and return event"""
    event=Event(friend=friend, etype=etype, details=details, date=date)

    db.session.add(event)
    db.session.commit()

    return event

def get_event_types():
    return Event_type.query.all()

def get_etype_by_key(event_key):
    return Event_type.query.get(event_key)

def get_friend_types():
    return Friend_type.query.all()

def get_friend_type_by_key(friend_key):
    return Friend_type.query.get(friend_key)

if __name__ == '__main__':
    from flask import Flask

    connect_to_db(app)