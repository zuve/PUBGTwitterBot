import tweepy, praw, os, requests

def substring_indexes(substring, string):
    last_found = -1
    while True:
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:
            break
        yield last_found

#Logging variables
writeTweetLog = open("log.txt", "a")
readTweetLog = open("log.txt", "r")

writeLinkLog = open("linkLog.txt", "a")
readLinkLog = open("linkLog.txt", "r")

posted = [post.rstrip("\n") for post in readTweetLog]
postedLinks = [link.rstrip("\n") for link in readLinkLog]

readTweetLog.close()
readLinkLog.close()

#Twitter variables
TWITTER_CONSUMER_KEY = os.environ["PUBGBOT_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["PUBGBOT_CONSUMER_SECRET"]
TWITTER_ACCESS_KEY = os.environ["PUBGBOT_ACCESS_KEY"]
TWITTER_ACCESS_SECRET = os.environ["PUBGBOT_ACCESS_SECRET"]
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)
pubg_twitter = 882248998547070981
recent_tweets = api.user_timeline(user_id=pubg_twitter, page=1, tweet_mode="extended")

#Reddit variables
REDDIT_CLIENT_ID = os.environ["PUBGBOT_REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = os.environ["PUBGBOT_REDDIT_CLIENT_SECRET"]
REDDIT_USERNAME = os.environ["REDDIT_USERNAME"]
REDDIT_PASSWORD = os.environ["REDDIT_PASSWORD"]
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, password=REDDIT_PASSWORD, user_agent="PUBG Twitter Bot 0.1", username=REDDIT_USERNAME)
subreddit = reddit.subreddit("PUBATTLEGROUNDS")

for t in recent_tweets:
    recent_tweet = h.unescape(t.full_text)
    recent_tweet_url = "https://twitter.com/statuses/" + str(t.id)
    recent_tweet_id = str(t.id)
    reply_status = t.in_reply_to_status_id
    steamLinks = list(url["expanded_url"] for url in t.entities["urls"] if "steamcommunity" in url["expanded_url"])
    if reply_status is None or int(api.get_status(reply_status).user.id_str) == pubg_twitter:
        if len(steamLinks) > 0:
            for url in steamLinks:
                r = requests.get(url).content
                titleBaseIndex = r.index('<h2 class="large_title"')
                titleStartIndex = r.index('>', titleBaseIndex) + 1
                titleEndIndex = r.index('<', titleStartIndex)
                title = r[titleStartIndex:titleEndIndex]
                if ("PC 1.0 Update" in title or "Dev Letter" in title or "Dev Blog" in title or "Patch Notes" in title) and not any(url in l for l in postedLinks):
                    writeLinkLog.write(url)
                    video_indexes = list(substring_indexes("dynamiclink_box", r))
                    if len(video_indexes) > 0:
                        video_comment = "Youtube videos in this announcement:\n\n"
                        for i in video_indexes:
                            linkStartIndex = r.index("&quot;", i) + 6
                            linkEndIndex = r.index("&quot;", linkStartIndex)
                            link = "https://www.youtube.com/watch?v=" + r[linkStartIndex:linkEndIndex]
                            linkTitleStartIndex = r.index('<\/span>', linkEndIndex) + 8
                            linkTitleEndIndex = r.index("&nbsp;", linkTitleStartIndex)
                            linkTitle = r[linkTitleStartIndex:linkTitleEndIndex]
                            video_comment += "[" + linkTitle + "]" + "(" + link + ")\n\n"
                    post = subreddit.submit(title, url=url).flair.select("ba18c8f4-14b8-11e7-a6c6-0e11d8c4f614", text=None)
                    post.reply(video_comment)
writeTweetLog.close()
writeLinkLog.close()
