from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import os
from twilio.rest import Client
import cloudinary


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
messaging_sid = os.environ['messaging_service_sid']
cloud_name = os.environ['cloud_name']
cloud_api_key = os.environ['cloud_api_key']
cloud_api_secret = os.environ['cloud_api_secret']

my_cloudinary = cloudinary.config( 
  cloud_name = cloud_name, 
  api_key = cloud_api_key, 
  api_secret = cloud_api_secret 
)


@app.route('/')
def show_login():
    """Show app's login page"""
    return render_template("login.html")

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

@app.route('/users/<user_id>/friends')
def show_users_friends_list(user_id):
    """display list of friends"""
    friends = crud.get_friends_by_user_id(user_id)
    return render_template('friends_list.html', friends = friends)

@app.route('/friends/add-friend')
def add_friend_form():
    """form where user can add a new friend"""
    types = crud.get_friend_types()
    return render_template('add_friend.html', types = types)

@app.route('/friends', methods=['POST'])
def add_friend():
    """add friend to database"""
    user_id = session['user_id']
    print(user_id)
    user = crud.get_user_by_id(user_id)
    print(user)
    print(type(user))
    friend_key = request.form.get('friend_type')
    ftype = crud.get_friend_type_by_key(friend_key)
    full_name = request.form.get('name')
    bday = request.form.get('bday')
    date_met = request.form.get('met')
    picture = request.form.get('pic')
    print(picture)
    likes = request.form.get('likes')
    dislikes = request.form.get('dislikes')

    crud.create_friend(user, ftype, full_name, bday, date_met, picture, 
                  likes, dislikes)

    return redirect(f'/users/{user_id}/friends')

@app.route('/friends/<friend_id>') 
def show_friend_details(friend_id):
    """display details about specific friend"""
    # friend = crud.get_friend_by_friend_id(friend_id)
    friend = crud.get_friend_by_friend_id(friend_id)

    return render_template('friend_details.html', friend = friend)

@app.route('/events/add-event')
def add_event_form():
    types = crud.get_event_types()
    user_id = session['user_id']
    friends = crud.get_friends_by_user_id(user_id)
    return render_template('add_event.html', types = types, friends = friends)

@app.route('/events', methods=['POST'])
def add_event():

    friend_id = request.form.get('friend')
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

    return redirect('/texts/send-text')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)