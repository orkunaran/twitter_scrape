# import necessary libraries
import configparser
import tweepy as tw
import pandas as pd
import csv #to write tweets to csv

# read twitter.txt to get keys, SAVE YOUR API KEY somewhere else to be safe
config = configparser.RawConfigParser()
config.read(filenames = 'twitter.txt')

# read keys: your code should be:
# confit.get([] part in your txt, 'name of the token')
accesstoken = config.get('my section','access_token')
accesstokensecret = config.get('my section','access_token_secret')
apikey = config.get('my section','api_key')
apisecretkey = config.get('my section','api_secret')

# set authentication
auth = tw.OAuthHandler(apikey,apisecretkey)
auth.set_access_token(accesstoken,accesstokensecret)
api = tw.API(auth,wait_on_rate_limit=True) # wait_on_rate_limit is mandatory to get lots of tweetw with one run.

# check if we get the authentication correct
print(api.verify_credentials().screen_name)
# should print your twitter user name

# my project was to scrape tweets about MonkeyPox
search_word = '#monkeypox' #simple tweeter interface for topic search
date_since = '2022-05-22' #you can only get tweets from 1 week back to date

#let's get into work


# Open/create a file to append data to
csvFile = open('million_tweets.csv', 'a')

#Use csv writer
csvWriter = csv.writer(csvFile)
tweets = tw.Cursor(api.search_tweets,
                   q = search_word,
                   lang ='en',
                   until = date_since,
                   tweet_mode = 'Extended').items(50000)

for tweet in tweets:
    # Write a row to the CSV file.
    # I scraped 50000 tweets in 14 iterations. 15 minutes wait time is automatically generated by tweepy
    # it contiunes by itself
    csvWriter.writerow([tweet.created_at, #get tweet time
                        tweet.user.screen_name,  #user name
                        tweet.user.location, # location
                        tweet.user.created_at, # user join date
                        tweet.user.friends_count, #followed count
                        tweet.user.followers_count, #followers count
                        tweet.user.statuses_count, #total tweets count
                        tweet.text.encode('utf-8')]) # the tweet
csvFile.close()


column_names = ['date','nick_name','location','tweet_at','friends','followers','total_tweets','tweet']
twits = pd.read_csv('million_tweets.csv', names = column_names)

