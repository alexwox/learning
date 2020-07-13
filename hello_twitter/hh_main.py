#Run
import tweepy as tw
from datetime import datetime
from time import sleep
import hh_config as hc

auth = tw.OAuthHandler(hc.API_key, hc.API_secret_key)
auth.set_access_token(hc.access_token, hc.access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
print("Starting up")
print("------------")
while True:
    i = 0
    for status in api.home_timeline():
        try:
            api.retweet(status.id)
            i += 1
            print("\n")
            print("New tweet: ")
            print(str(datetime.now()) + ",  " + str(status.id))
            print(str(status.author.screen_name) + ",  " + str(status.text))
            print("\n")
        except:
            if round(int(datetime.now().second)) == 0:
                print("No new tweets, " + str(datetime.now())) 
                sleep(1)
            continue

