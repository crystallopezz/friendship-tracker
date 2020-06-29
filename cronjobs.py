from model import connect_to_db, Reminder, app
import logging
from server import crontab
from pathlib import Path
import time
import os

logging.basicConfig(filename='/home/vagrant/src/friendship_tracker/project.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
connect_to_db(app)
crontab.init_app(app)
logger.debug(crontab.app.config['SQLALCHEMY_DATABASE_URI'])

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
    do_something()
    return