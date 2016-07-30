import tweepy
import csv

# Twitter API credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''


def scrap_all_tweets(hashtag,since,until):

    # access twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, retry_count=15, retry_delay=100000, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # list to hold all the tweets
    base_tweets = []

    # hold recent tweets (100 maximum allowed count)
    new_tweets = api.search(q=hashtag, since=since, until=until, count=100)

    # save most recent tweets
    base_tweets.extend(new_tweets)

    # hold the id of oldest tweet
    oldest = base_tweets[-1].id - 1

    # scrap tweets until there are nothing left
    while len(new_tweets) > 0:
        print "scraped tweets before %s" % (oldest)

        # further requests use the max_id param to prevent duplicates
        new_tweets = api.search(q=hashtag, since=since, until=until, count=100, max_id=oldest)

        # store the most recent tweets
        base_tweets.extend(new_tweets)

        # update the oldest tweet id
        oldest = base_tweets[-1].id - 1

        print "...%s tweets scraped so far" % (len(base_tweets))

    # transform the tweets to populate the csv
    out_fields = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.user.screen_name,
                  tweet.user.followers_count, tweet.lang, tweet.user.location.encode("utf-8"),
                  tweet.place.country if tweet.place != None else None, tweet.retweet_count, tweet.favorite_count]
                 for tweet in base_tweets]

    # write the csv
    #current_working_dir = "C:/Users/607949405/Documents/test45/final/"
    #log_tweets = current_working_dir + 'test.csv'
    #with open(log_tweets, 'wb') as f:
    with open('%s_tweets.csv' % hashtag, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "screen_name", "followers_count", "lang", "location", "country",
                         "retweet_count", "favorite_count"])
        writer.writerows(out_fields)
    pass


if __name__ == '__main__':
    # pass in the hastag that you want to download since, until params
    scrap_all_tweets("#kabali",since="2016-07-25", until="2016-07-26")
