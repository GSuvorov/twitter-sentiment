# coding=utf-8

import json 
import os
import random

from sklearn import svm
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.utils import compute_class_weight
from sklearn.naive_bayes import GaussianNB

from numpy import *
import re
from . import informator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SentimentAnalyzer:

	def __init__(self):
		self.simples = [
				'?', '!', '.', '*'
		]
		self.regexen = [ 
			re.compile(u'[А-Я][^А-Я]', re.UNICODE), # Uppercase capital letters 
			re.compile(u'[А-Я]{3,}', re.UNICODE), # CAPS
			re.compile('[:=][\|/]'), # =\
			re.compile('[:=;]-?[)DpP\]]'), # :-) :p :]
			re.compile("[:=][-']?[(]"), # :'( :(
			re.compile('[(]-?[:=;]'), # (: 
			re.compile('[D)]-?[:=;]'), # D: 
			re.compile('\S{2,}\.(com|ru|org|net|ua|co|su)\S*'), # link
			re.compile('\S{2,}\.(com|ru|org|net|ua|co|su)\S*$') # link at the end
		]
	def get_polarity(self, json_tweet):
		pol = json_tweet['polarity']
		if pol == "negative":
			return -1
		elif pol == 'positive':
			return +1
		else:
			return 0

	def polarity_to_num(self, label):
		if label < -0.5:
			return 'negative'
		elif label > 0.5:
			return 'positive'
		else:
			return 'neutral'

	def get_featutes_string(self, string, p=False):
		ans = []
		ans += [string.count(')') - string.count('(')]
		for sub in self.simples:
			ans += [string.count(sub)]
		if p:
			print(string)
		for regex in self.regexen:
			if p:
				print(regex.findall(string), regex.pattern)
			res = regex.findall(string)
			ans += [len(res)]
			if p:
				print(regex.findall(string), regex.pattern)
		return ans
	
	def get_features(self, corpus):
		return list(map(lambda x: self.get_featutes_string(x['text'], False), corpus))

	def train(self, training_corpus):
		self.classifier = svm.SVC(class_weight='balanced')
		arrX = array(self.get_features(training_corpus), dtype = float64)
		arrY = array(list(map(self.get_polarity, training_corpus)), dtype = float64)
		self.classifier.fit(preprocessing.scale(arrX), arrY)

	def getClasses(self, texts):
		x = array(list(map(lambda x: self.get_featutes_string(x), texts)), dtype = float64)
		
		return list(map(self.polarity_to_num, self.classifier.predict(preprocessing.scale(x))))

training_corpus = json.load(open(os.path.join(BASE_DIR ,'algorythm/tweets.json')))

def cross_validate(json_corpus):
	for k in range (0, 5):
		i = k * len(json_corpus) / 5
		j = (k + 1) * len(json_corpus) / 5
		analyzer = SentimentAnalyzer()
		analyzer.train(training_corpus[:int(i)] + training_corpus[int(j):])
		classes = analyzer.getClasses(list(map(lambda x: x['text'], training_corpus[int(i):int(j)])))
		classes = list(classes)
		corr = 0
		l = -1
		for tweet in training_corpus[int(i):int(j)]:
			if tweet['polarity'] == classes[1]:
				corr += 1
		# print(corr * 1. / (j - i))


def get_sentiment(person, count):
	sentiments = dict()

	cross_validate(training_corpus)
	# random.shuffle(training_corpus)
	analyzer = SentimentAnalyzer()

	informator.getPerson(person, count)
	analyzer.train(training_corpus)
	person_corpus = json.load(open('_data.json'))

	positive = analyzer.getClasses(map (lambda x: x['text'], person_corpus)).count("positive")/len(person_corpus)
	negative = analyzer.getClasses(map (lambda x: x['text'], person_corpus)).count("neutral")/len(person_corpus)
	neutral = analyzer.getClasses(map (lambda x: x['text'], person_corpus)).count("negative")/len(person_corpus)
	
	sentiments["positive"] = positive
	sentiments["negative"] = negative
	sentiments["neutral"] = neutral

	for key in sentiments.keys():
		print (key + ": " + str(sentiments.get(key)))

	return sentiments

get_sentiment("сергей шнуров", 10)
