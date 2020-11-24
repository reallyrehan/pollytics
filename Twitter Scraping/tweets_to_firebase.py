import json
import requests

f = open('Tweets/biden_tweets.json','r',encoding='UTF-8')
trump_tweets = json.load(f)
f.close()

#result_message = requests.put('https://data-management-ac8c8.firebaseio.com/tweets/biden.json',json.dumps(trump_tweets))