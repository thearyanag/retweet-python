import time
import requests
from requests_oauthlib import OAuth1
import config
import random
import sqlite3
import sql_helper

consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
oauth_token=config.oauth_token
oauth_token_secret=config.oauth_token_secret
bearer_token=config.bearer_token

# uses bearer authentication to get tweets from the user
# returns list of tweetids and a list of pagination token if found else returns 404
# example response ['3434','5534534','5435345','5345'...10 tweet ids],['next_token','previous_token']

def get_tweets(user_id):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    BASE_URL=f"https://api.twitter.com/2/users/{user_id}/tweets"
    response=requests.get(BASE_URL , headers=headers).json()
    tweet_data=response['data']
    tweet_ids=[]
    tweet_meta=response['meta']
    tweet_paginate=[]

    for each_tweet in tweet_data:
        tweet_ids.append(each_tweet['id'])

    try:
        tweet_paginate.append(tweet_meta['next_token'])
    except Exception as e:
        print(e)
        tweet_paginate=404
    try:
        tweet_paginate.append(tweet_meta['previous_token'])
    except:
        print()

    return tweet_ids,tweet_paginate

# same as get_tweets except gives tweets after a given pagination token
def get_tweets_paginate(user_id,pagination_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    BASE_URL=f"https://api.twitter.com/2/users/{user_id}/tweets?pagination_token={pagination_token}"
    response=requests.get(BASE_URL , headers=headers).json()
    tweet_data=response['data']
    tweet_ids=[]
    tweet_meta=response['meta']
    tweet_paginate=[]

    for each_tweet in tweet_data:
        tweet_ids.append(each_tweet['id'])

    try:
        tweet_paginate.append(tweet_meta['next_token'])
    except Exception as e:
        print(e)
        tweet_paginate=404
    try:
        tweet_paginate.append(tweet_meta['previous_token'])
    except:
        print()

    return tweet_ids,tweet_paginate

# retweets a random tweet that has not already being tweeted by the user
# sql_helper is used to check wether tweet has already being tweeted or not

def retweet(userid):
    tweet_ids,paginate_tokens=get_tweets(userid)
    tweet_index=int(random.random()*10)
    id_to_tweet=tweet_ids[tweet_index]
    tweet_ids,paginate_tokens=get_tweets(userid)
    tweet_index=int(random.random()*10)
    id_to_tweet=tweet_ids[tweet_index]
    co=1

    while(sql_helper.checkpermit(id_to_tweet)):
        tweet_index=int(random.random()*10)
        id_to_tweet=tweet_ids[tweet_index]
        co=co+1
        if co>5 and paginate_tokens == 404:
            tweet_ids,paginate_tokens=get_tweets_paginate(userid,paginate_tokens[0])       
    sql_helper.givepermit(id_to_tweet)
    auth=OAuth1(consumer_key , consumer_secret , oauth_token , oauth_token_secret)
    BASIC_URL=f"https://api.twitter.com/1.1/statuses/retweet/{id_to_tweet}.json"
    print(requests.post(BASIC_URL,auth=auth))


# a script to auto-tweet at certain times a day from multiple accounts
# number of accounts can also be used as a list along with a list of time to tweet
while True:
    result=time.localtime()
    hour=result.tm_hour
    minute=result.tm_min
    sec=result.tm_sec

    if(hour == 6 and minute == 0 and sec == 0):
        id="" #tweet_id_1
        retweet(id)
        time.sleep(3600.0)
        
    if(hour == 10 and minute == 0 and sec == 0):
        id="" #tweet_id_2
        retweet(id)
        time.sleep(3600.0)
        

    if(hour == 14 and minute == 39 and sec == 0):
        id="" #tweet_id_3
        retweet(id)
        time.sleep(3600.0)

    if(hour == 18 and minute == 0 and sec == 0):
        id="" #tweet_id_4
        retweet(id)
        time.sleep(3600.0)

    if(hour == 22 and minute == 0 and sec == 0):
        id="" #tweet_id_5
        retweet(id)
        time.sleep(3600.0)
