from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

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


@app.route('/friends/<friend_id>') 
def show_friend_details(friend_id):
    """display details about specific friend"""
    friend = crud.get_friend_by_friend_id(session['user_id'], friend_id)

    return render_template('friend_details.html', friend = friend)

@app.route('/friends/add-friend')
def add_friend_form():
    """form where user can add a new friend"""
    types = crud.get_friend_types()
    return render_template('add_friend.html', types = types)

@app.route('/friends', methods=['POST'])
def add_friend():
    """add friend to database"""
    user = crud.get_user_by_id(1)
    ftype = request.form.get('friend_type')
    full_name = request.form.get('name')
    bday = request.form.get('bday')
    date_met = request.form.get('met')
    picture = request.form.get('pic')
    likes = request.form.get('likes')
    dislikes = request.form.get('dislikes')

    crud.create_friend(user, ftype, full_name, bday, date_met, picture, 
                  likes, dislikes)

    return redirect('/users/<user_id>/friends')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)