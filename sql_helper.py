import os
from re import T
from sqlalchemy import create_engine , text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, String, UnicodeText
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.sqltypes import Integer


# tweetid.db is the name of the database and can be replaced by anything you like , How about pancake.db ?

def start() -> scoped_session:
    engine = create_engine('sqlite:///tweetid.db')
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    print(
        "DB_URI is not configured. Features depending on the database might have issues."
    )
    print(str(e))

class Tweets(BASE):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True , autoincrement=True)
    tweet_id = Column(Integer, nullable=False)
    userid = Column(Integer, nullable=false)

    def __init__(self , tweetid , userid):
        self.tweet_id=tweetid
        self.userid=userid

Tweets.__table__.create(checkfirst=True)

# add tweet to sqlite database so that later we can check if the tweet has already been tweeted or not 
def addtweet(tweet_id,user_id): 
        adduser=Tweets(tweetid=tweet_id,userid=user_id)
        SESSION.add(adduser)
        SESSION.commit()

# check tweet from sqlite database so that we don't retweet it again (return tuple of tweet of found else returns None so can be checked using truthy values)
def checkpermit(tweet_id): 
    if SESSION.query(text(tweet_id)).filter(Tweets.tweet_id == tweet_id).one_or_none():
        return SESSION.query(text(tweet_id)).filter(Tweets.tweet_id == tweet_id).one_or_none()
    else:
        if SESSION.query(text(tweet_id)).filter(Tweets.tweet_id == tweet_id).one_or_none():
            return not (SESSION.query(text(tweet_id)).filter(Tweets.tweet_id == tweet_id).one_or_none())
