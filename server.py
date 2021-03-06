from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, app, Social_type
import crud
from jinja2 import StrictUndefined
import os
from twilio.rest import Client
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_crontab import Crontab

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
messaging_sid = os.environ.get('messaging_service_sid')
cloud_name = os.environ.get('cloud_name')
cloud_api_key = os.environ.get('cloud_api_key')
cloud_api_secret = os.environ.get('cloud_api_secret')

@app.route('/')
def show_login():
    """Show app's login page"""
    return render_template("login.html")

@app.route('/create-account')
def new_account_form(): 
    """show new account form"""
    return render_template("new_account.html")

@app.route('/users', methods=['POST'])
def login():
    """look for user by email and password"""
    email=request.form.get('email')
    input_pw=request.form.get('password')
    user = crud.get_user_by_email(email)
    user_id = user.user_id

    session['user_id'] = user_id

    if crud.validate_user_password(input_pw, email):

        return redirect(f'/users/{user_id}/friends')

    # TODO turn in to flash message
    # else: 
    #     return alert('Email or password is incorrect.')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """create new user"""
    email = request.form.get('email')
    pw=request.form.get('password')

    # TODO
    # if crud.get_user_by_email(email): 
    #     flash user with that email already exists

    crud.create_user(email, pw)

    return redirect("/")
    # TODO: create flash to say the account was created


@app.route('/users/<user_id>/friends')
def show_users_friends_list(user_id):
    """display list of friends"""
    friends = crud.get_friends_by_user_id(user_id)
    return render_template('friends_list.html', friends = friends, user_id=user_id)

@app.route('/friends/add-friend')
def add_friend_form():
    """form where user can add a new friend"""
    types = crud.get_friend_types()
    return render_template('add_friend.html', types = types)

@app.route('/friends', methods=['POST'])
def add_friend():
    """add friend to database"""
    
    my_cloudinary = cloudinary.config( 
        cloud_name = cloud_name, 
        api_key = cloud_api_key, 
        api_secret = cloud_api_secret 
    )

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)
    friend_key = request.form.get('friend_type')
    ftype = crud.get_friend_type_by_key(friend_key)
    full_name = request.form.get('name')
    bday = request.form.get('bday')
    date_met = request.form.get('met')

    photo_uploaded = request.files['pic']
    cloudinary_upload = cloudinary.uploader.upload(photo_uploaded)
    photo_url = cloudinary_upload['url']

    likes = request.form.get('likes')
    dislikes = request.form.get('dislikes')
    phone = request.form.get('phone_number')

    friend = crud.create_friend(user, ftype, full_name, bday, date_met, photo_url, 
                  likes, dislikes, phone)

    twitter = request.form.get('twitter')
    insta = request.form.get('insta')
    facebook = request.form.get('facebook')

    if twitter: 
        crud.create_social_account(friend, Social_type.query.get('twit'), twitter)

    if insta: 
        crud.create_social_account(friend, Social_type.query.get('insta'), insta)

    if facebook:
        crud.create_social_account(friend, Social_type.query.get('fb'), facebook)

    return redirect(f'/users/{user_id}/friends')

@app.route('/friends/<friend_id>') 
def show_friend_details(friend_id):
    """display details about specific friend"""

    friend = crud.get_friend_by_friend_id(friend_id)
    bday = friend.bday.strftime('%B, %d, %Y')
    date_met = friend.date_met.strftime('%B, %d, %Y')

    events = friend.events[::-1]
    print(events)

    session['friend_id'] = friend_id
    user_id = session['user_id']

    event_types = crud.get_event_types()

    return render_template('friend_details.html', friend = friend, bday=bday, date_met=date_met, user_id=user_id, events=events, types=event_types)

@app.route('/events/add-event/<friend_id>')
def add_event_form(friend_id):
    types = crud.get_event_types()
    friend = crud.get_friend_by_friend_id(friend_id)
    return render_template('add_event.html', types = types, friend = friend)

@app.route('/events', methods=['POST'])
def add_event():

    friend_id = session['friend_id']
    friend = crud.get_friend_by_friend_id(friend_id)

    event_key = request.form.get('event_type')
    etype = crud.get_etype_by_key(event_key)

    details = request.form.get('details')
    date = request.form.get('event_date')

    crud.create_event(friend, etype, details, date)

    return redirect(f'/friends/{friend_id}')

@app.route('/texts/send-text')
def send_text_form():
    return render_template('text_form.html')

@app.route('/texts', methods=['POST'])
def send_text():
    body = request.form.get('message')
    to = request.form.get('phone_number')

    client = Client(account_sid, auth_token)

    message = client.messages \
                .create(
                     body=body,
                     from_="+12058469126",
                     to=to
                )

    print(message.sid)

    friend_id=session["friend_id"]

    return redirect(f'/friends/{friend_id}')

@app.route('/reminders/add-reminder')
def reminder_form():
    """show reminder form"""
    return render_template('create_reminder.html')

@app.route('/reminders', methods=['POST'])
def create_reminder():
    reminder_name = request.form.get('reminder_name')
    date = request.form.get('reminder_time')

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    friend_id=session['friend_id']

    crud.create_reminder(user, reminder_name, date)

    return redirect(f'/friends/{friend_id}')

crontab = Crontab()
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)