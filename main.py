import tweepy, praw, os, json
from HTMLParser import HTMLParser

#HTML Parser for Tweet Text/Reddit Title
h = HTMLParser()

#Logging variables
log = open("log.txt", "r+")

posted = [post.rstrip('\n') for post in log]

#Twitter variables
TWITTER_CONSUMER_KEY = os.environ['PUBGBOT_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['PUBGBOT_CONSUMER_SECRET']
TWITTER_ACCESS_KEY = os.environ['PUBGBOT_ACCESS_KEY']
TWITTER_ACCESS_SECRET = os.environ['PUBGBOT_ACCESS_SECRET']
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)
pubg_twitter = 719324795167309827
recent_tweets = api.user_timeline(user_id=pubg_twitter, page=1)

#Reddit variables
REDDIT_CLIENT_ID = os.environ['PUBGBOT_REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['PUBGBOT_REDDIT_CLIENT_SECRET']
REDDIT_USERNAME = os.environ['REDDIT_USERNAME']
REDDIT_PASSWORD = os.environ['REDDIT_PASSWORD']
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, password=REDDIT_PASSWORD, user_agent='PUBG Twitter Bot 0.1', username=REDDIT_USERNAME)
subreddit = reddit.subreddit("PUBATTLEGROUNDS")

log = open("log.txt", "r+")
for t in recent_tweets:
    recent_tweet = h.unescape(t.text)
    recent_tweet_url = "https://twitter.com/statuses/" + str(t.id)
    recent_tweet_id = str(t.id)
    if "pushed a hotfix" in recent_tweet or "pushed an update" in recent_tweet or "resolved" in recent_tweet or "fixed the bug" in recent_tweet:
        if not any(recent_tweet_id in s for s in posted):
            subreddit.submit(recent_tweet, url=recent_tweet_url).flair.select('ba18c8f4-14b8-11e7-a6c6-0e11d8c4f614', text=None)
            log.write(recent_tweet_id + "\n")
