# coding=utf-8

import json
import tweepy
from tweepy.parsers import JSONParser

searched_tweets = list()

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

	# нужно написать\скачать модуль для перевода в транслит

	# searched_tweets = []
	# last_id = -1
	# while len(searched_tweets) < max_tweets:
	#     count = max_tweets - len(searched_tweets)
	#     try:
	#         new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
	#         if not new_tweets:
	#             break
	#         searched_tweets.extend(new_tweets)
	#         last_id = new_tweets[-1].id
	#     except tweepy.TweepError as e:
	#         break

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

