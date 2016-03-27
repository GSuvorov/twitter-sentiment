# coding=utf-8
import json 
import os

from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
import sklearn.feature_extraction.text
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
# from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import *

from . import informator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SentimentAnalyzer:

	def train(self,corpus):
		self.le = preprocessing.LabelEncoder()
		text = list(map (lambda x: x['text'], corpus))
		polarity = list(map(lambda x: x['polarity'], corpus))
		
		self.le.fit(text)
		y_train = self.le.fit_transform(polarity)
		# print(self.le.inverse_transform(y_train))
		cv =  cross_validation.StratifiedKFold(y_train, n_folds=10)

		# С ngram_range можно поэкспериментировать
		self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(1, 2))

		X_train = self.vectorizer.fit_transform(text)
		self.classifier = SGDClassifier().fit(X_train, y_train)
		# self.classifier = MultinomialNB().fit(X_train, y_train)

		# print(vectorizer.inverse_transform(X_train))
	def getClasses(self, corpus):
		text = list(map(lambda x: x['text'], corpus))
		x = self.vectorizer.transform(text)
		# print(self.vectorizer.inverse_transform(x))
		pred = self.classifier.predict(x)
		
		# print(pred.tolist())
		return pred.tolist()
training_corpus = json.load(open(os.path.join(BASE_DIR ,'algorythm/tweets.json')))

def get_sentiment(person, count):
	sentiments = dict()

	analyzer = SentimentAnalyzer()

	informator.getPerson(person, count)
	analyzer.train(training_corpus)
	person_corpus = json.load(open('_data.json'))
	result = analyzer.getClasses(person_corpus)
	positive = result.count(3)/len(person_corpus)
	neutral = result.count(2)/len(person_corpus)
	negative = result.count(1)/len(person_corpus)	
	sentiments["positive"] = positive
	sentiments["neutral"] = neutral
	sentiments["negative"] = negative


	for key in sentiments.keys():
		print (key + ": " + str(sentiments.get(key)))

	return sentiments

# get_sentiment("сергей шнуров", 10)
