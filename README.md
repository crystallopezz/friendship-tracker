# friendly
Friendly is a tool designed to help users maintain meaningful relationships. Users keep track of details about their friends and details of when they last interacted with their friend, with text reminders to contact their friend and the ability to send texts from within the app using Twilio’s API.

# About Me
As a kid, Crystal spent a lot of time on Neopets (a website  in the early '00s where you have a virtual pet) and really liked changing up her profile but didn’t like any of the existing profile templates. So, she learned some basic HTML to create her own custom profiles. 15 years later in the real world, Crystal was the first support representative at a fintech startup  She spent a lot of time  debugging technical problems with the APIs. Unfortunately, Crystal was passed up for a promotion because she didn't have a technical education. 
This was a wakeup call for Crystal as understood that continuing her former interest would be a good way to open up her  career opportunities. She left her job shortly after pursue software engineering.

# Technologies
* Python
* Flask
* Jinja2
* PostgresQL
* SQLAlchemy
* HTML
* CSS
* Bootstrap
* Twilio
* Cloudinary
* Arrow
* Flask-Crontab

# Features
App Demo can be found here: https://www.youtube.com/watch?v=0Q46ANF7mBs&t=1s
List of features below

## Login
![Login Image](https://github.com/crystallopezz/friendship-tracker/blob/master/Login.png)

## Friend List
![Friend List](https://github.com/crystallopezz/friendship-tracker/blob/master/Friend%20List.png)

## Adding a Friend
Easily add a new friend to track. Include their basic information, interests and socials.

![Adding Friend](https://github.com/crystallopezz/friendship-tracker/blob/master/Add%20New%20Friend.png)

## Friend Profile
View a specific friend's information and a timeline of your logged events with them in one place. This page is where the next three features live.

![Friend Profile](https://github.com/crystallopezz/friendship-tracker/blob/master/Friend%20Profile.png)

## Adding A New Event
Log a new event with your friend including the date and event details. The new event will automatically show up in your timeline.

![AddEvent1](https://github.com/crystallopezz/friendship-tracker/blob/master/Add%20Event.png)
![AddEvent2](https://github.com/crystallopezz/friendship-tracker/blob/master/Add%20Event%202.png)

## Texting Friend
Text your friend from within the app using Twilio's API!

![TextFriend1](https://github.com/crystallopezz/friendship-tracker/blob/master/Send%20Text.png)
![TextFriend2](https://github.com/crystallopezz/friendship-tracker/blob/master/Send%20Text%202.png)

## Setting up Reminders
Set up a text reminder related to your friend from within the app using Twilio's API.

![Reminder1](https://github.com/crystallopezz/friendship-tracker/blob/master/Reminder%201.png)
![Reminder2](https://github.com/crystallopezz/friendship-tracker/blob/master/Reminder%202.png)


# Installation
To run friendly, continue reading!

1. Install PostgresQL (Mac OSX)

2. Clone or fork this repo: 
````https://github.com/crystallopezz/friendship-tracker.git````

3. Create and activate a virtual environment inside your friendly directory:
````
virtualenv env
source env/bin/activate
````

4. Install the dependencies: 
````pip install -r requirements.txt````

5. Sign up to use Cloudinary and Twilio's API
Cloudinary: https://cloudinary.com/users/register/free
Twilio: https://www.twilio.com/try-twilio

6. Save your API keys in a file called secrets.sh using this format:

````
export account_sid="TWILIO_ACCOUNT_SID_HERE"
export auth_token="TWILIO_AUTH_TOKEN_HERE"
export cloud_name="CLOUDINARY_CLOUD_NAME_HERE"
export cloud_api_key="CLOUDINARY_API_KEY_HERE"
export cloud_api_secret="CLOUDINARY_API_SECRET_HERE"
````

7. Source your keys from your secrets.sh file into your virtual environment:

````source secrets.sh````

8. Set up the database:

````
createdb friendlydb
python3 model.py
````

9. Crontab setup: 

* add the cronjob to the crontab using flask-crontab:
````
export FLASK_APP=cronjobs.py
flask crontab add
````

* provide the job with Twilio API keys: 
````
tbd
````

10. Run the app: 
````python3 server.py````

11. You can now navigate to 'localhost:5000/' to access friendly!
