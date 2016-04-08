# coding=utf-8

import json
import tweepy
from tweepy.parsers import JSONParser

searched_tweets = list()
# Скрипт, для получения твитов, стандартное API позволяет выкачать только 100. Нужно думать, как качать больше
def getPerson(person, count):
	consumer_key = "vAFqO3jFbVUXkSVKSitaUiU4Q"
	consumer_secret = "4aG1sNq2pwDjEvpvG7FbR63GMCrQQfbTkP8Z0kdrLvkE8MCv8A"
	access_key="711632049711554560-Co5AtwXqrg5Qf3m2TwAzHnw6C5rWfxS"
	access_secret="VXMe4nJKHX1mb8QNh5LW3TMAdZSQ0L9FuwZADlG6GxHFB"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api=tweepy.API(auth, parser = JSONParser())
	# api=tweepy.API(auth)

	query = person
	max_tweets = count

	new_tweets = api.search(q=query, count=count)
	file = open('_data.json' , 'w')

	json_str = json.dumps(new_tweets['statuses'], indent = 4, sort_keys = True)
	# print(json_str)
	file.write(u''.join(json_str))
	file.close()

def get_tweets_list():
	tweets = json.load(open("_data.json", "r"))
	for tweet in tweets:
		searched_tweets.append(tweet["text"])
	return searched_tweets

