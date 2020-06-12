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
    user_id = crud.get_user_id(email)
    # get user by email ^

    session['user_id'] = user_id


    if crud.validate_user_password(input_pw, email):

        #TODO add user ID to session

        return redirect(f'/friends/{user_id}')

    # TODO turn in to flash message
    # else: 
    #     return alert('Email or password is incorrect.')

@app.route('/friends/<user_id>')
# users/user_id/friends
def show_users_friends_list(user_id):
    friends = crud.get_friends_by_user_id(user_id)
    return render_template('friends_list.html', friends = friends)

# friends/friend_id
@app.route('/friend/<friend_id>') 
def show_friend_details(friend_id):
    friend = crud.get_friend_by_friend_id(session['user_id'], friend_id)

    return f"<h1>hello {friend.full_name}</h2>"


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)