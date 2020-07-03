import os
import json
from datetime import datetime
import crud
import model
from flask import Flask

os.system('dropdb friendshiptracker')
os.system('createdb friendshiptracker')

model.connect_to_db(model.app)
model.db.create_all()

# seed event_types table

event_types_in_db = []
with open('data/event_types.json') as etypes:
    etype_data = json.loads(etypes.read())

for etype in etype_data:

    event_key = etype['event_key']
    event_type = etype['event_type']

    db_etype = crud.create_event_type(event_key, event_type)

    event_types_in_db.append(db_etype)

# seed friend_types table
friend_types_in_db = []
with open('data/friend_types.json') as ftypes:
    ftype_data = json.loads(ftypes.read())

for ftype in ftype_data: 

    friend_key = ftype['friend_key']
    name = ftype['name']

    db_ftype = crud.create_friend_type(friend_key, name)

    friend_types_in_db.append(db_ftype)

# seed social_types table
social_types_in_db = []
with open('data/social_type.json') as stypes:
    stype_data = json.loads(stypes.read())

for stype in stype_data:

    social_type = stype['social_type']
    name = stype['name']
    logo = stype['logo']

    db_stype = crud.create_social_type(social_type, name, logo)

    social_types_in_db.append(db_stype)

# seed user table
with open('data/users.json') as users:
    user_data = json.loads(users.read())

for user in user_data: 

    email = user['email']
    password = user ['password']

    db_user = crud.create_user(email, password)

# seed friends table
with open('data/friends.json') as friends:
    friend_data = json.loads(friends.read())

for friend in friend_data:
        
    user = db_user

    ftype = model.Friend_type.query.get(friend['ftype'])

    full_name = friend['full_name']

    bday = datetime.strptime(friend['bday'], '%Y-%m-%d')

    date_met = datetime.strptime(friend['date_met'], '%Y-%m-%d')

    picture = friend['picture']

    likes = friend['likes']

    dislikes = friend['dislikes']

    crud.create_friend(user, ftype, full_name, bday, date_met, picture, 
                  likes, dislikes)

# seed events table
with open('data/events.json') as events:
        event_data = json.loads(events.read())

for event in event_data:

    friend = model.Friend.query.filter_by(full_name=event['friend']).first()

    etype = model.Event_type.query.get(event['etype'])

    details = event['details']

    date = datetime.strptime(event['date'], '%Y-%m-%d')

    crud.create_event(friend, etype, details, date)

#seed social_medias table
with open('data/social_medias.json') as socials:
        social_data = json.loads(socials.read())

for social in social_data:

    friend = model.Friend.query.filter_by(full_name=social['friend']).first()
    stype = model.Social_type.query.get(social['stype'])
    url = social['url']

    crud.create_social_account(friend, stype, url)


























