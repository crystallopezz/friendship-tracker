from model import connect_to_db, Reminder, app
import logging
from server import crontab, account_sid, auth_token, messaging_sid
from pathlib import Path
import time
import os
import arrow
from twilio.rest import Client

logging.basicConfig(filename='/home/vagrant/src/friendship_tracker/project.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
connect_to_db(app)
crontab.init_app(app)
logger.debug(crontab.app.config['SQLALCHEMY_DATABASE_URI'])

def check_reminders():
    logger.debug("starting job")
    to_send = Reminder.query.filter(Reminder.sent == None).all()
    now = arrow.now('US/Pacific')
    for reminder in to_send:
        date = arrow.get(reminder.date)
        if date <= now:

            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                     body=f'Reminder to: {reminder.reminder_name}',
                     from_="+12058469126",
                     to="+14159489652"
                )

                # reminder.sent = arrow.now('US/Pacific').datetime


















def do_something_else(to_be_sent):
  for item in to_be_sent:
        Path(f'/home/vagrant/src/friendship_tracker/{time.time()}-{item.reminder_name}').touch()

def do_something():
    # find the time now
    # now = arrow.now('US/Pacific')

    # def turn_pacific(time): 
    #   arrow.get(time, 'US/Pacific')

    logger.debug("do something")
    # logger.debug()
    # Path(f'/home/vagrant/src/friendship_tracker/{time.time()}-start').touch()
    to_be_sent = Reminder.query.filter(Reminder.sent == None).all()
    
    do_something_else(to_be_sent)

    Path(f'/home/vagrant/src/friendship_tracker/{time.time()}-end').touch()

    return

@crontab.job()
def my_scheduled_job():
    logger.debug("starting job")
    logger.debug(os.environ)
    check_reminders()
    return