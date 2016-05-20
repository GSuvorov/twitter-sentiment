# coding=utf-8
import json
import hashlib
import tweepy
from tweepy.parsers import JSONParser

from . import translit

searched_tweets = list()
# Скрипт, для получения твитов, стандартное API позволяет выкачать только 100. Нужно думать, как качать больше
def get_person(person, count):
    consumer_key = "vAFqO3jFbVUXkSVKSitaUiU4Q"
    consumer_secret = "4aG1sNq2pwDjEvpvG7FbR63GMCrQQfbTkP8Z0kdrLvkE8MCv8A"
    access_key="711632049711554560-Co5AtwXqrg5Qf3m2TwAzHnw6C5rWfxS"
    access_secret="VXMe4nJKHX1mb8QNh5LW3TMAdZSQ0L9FuwZADlG6GxHFB"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api=tweepy.API(auth, parser = JSONParser())
    query = person
    max_tweets = count

    # запрос твитов
    new_tweets = api.search(q=query, count=count)

    # json для записи исходных твитов в базу данных
    person = person.replace(" ", "_").lower()

    file_name = 'JSON/raw_data_' + translit.translit(person)
    file = open(file_name + '.json' , 'w')
    json_str = json.dumps(new_tweets['statuses'], indent = 4, sort_keys = True)
    file.write(u''.join(json_str))
    file.close()

    # список для приведения твитов в "человеческий" вид
    all_tweets = list()
    for tweet in new_tweets["statuses"]:
        all_tweets.append(tweet["text"])

    prepare_to_learn(all_tweets, translit.translit(person))

def prepare_to_learn(tweets_list, person):
    if len(tweets_list) == 0:
        return 0

    all_tweets = [] # список полученных твитов
    hash_tweets = [] # хеши полученных твитов
    dict_tweets = {} # словарь по типу {ключ - хэш : значение - твит}
    tweets_json = [] # список для формирования json - объекта

    for tweet  in tweets_list:
        if len(tweet) == 0:
            continue
        all_tweets.append(tweet.lower())
        hash_tweets.append(hashlib.md5(tweet.encode()).hexdigest())

    for i in range(len(all_tweets)):
        dict_tweets[hash_tweets[i]] = all_tweets[i]

    # собираем json - объект
    for value in dict_tweets.values():
        tweets_json.append({"text": value})
    json_data = json.dumps(tweets_json, indent = 4, sort_keys = True)

    file = open("JSON/data_" + person + ".json", "w")
    file.write(json_data)
    file.close()

def get_tweets_list(person):
    person = person.replace(" ", "_")
    person = translit.translit(person.lower())
    tweets = json.load(open("JSON/data_" + person + ".json", "r"))
    for tweet in tweets:
        searched_tweets.append(tweet["text"])
    return searched_tweets
