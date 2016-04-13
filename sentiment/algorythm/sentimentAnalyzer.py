# coding=utf-8
import json 
import os

from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
import sklearn.feature_extraction.text
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
# from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import *

from . import informator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Непосредственно анализатор твитов
class SentimentAnalyzer:

    # Метод для обучения тренировочной выборки -- выборки твитов, с заранее размеченной "тональностью"

	def train(self,corpus):
		self.le = preprocessing.LabelEncoder()
		text = list( map (lambda x:x['text'], corpus))
		polarity = list(map(lambda x: x['polarity'], corpus))
		self.le.fit(text)
		# Приводим в порядок классы тренировочной выборки
		y_train = self.le.fit_transform(polarity)
		print(self.le.inverse_transform(y_train))
		cv =  cross_validation.StratifiedKFold(y_train, n_folds=10)
		self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(1, 2))
		# Векторизуем объекты тренировочной выборки
		X_train = self.vectorizer.fit_transform(text)
		self.classifier = SGDClassifier().fit(X_train, y_train)

    # Метод, для получения предикатов тестовой (или рабочей) выборки. Короче говоря, здесь твиты, которые сюда попали
		# получают "предсказание" о том, какой же они тональности являются. Этот предикат получается благодаря тому, что
	# мы обучили классификатор предыдущем методом на тренировочной выборке.
	def getClasses(self, corpus):
		text = list(map(lambda x:x['text'], corpus))
		if not text:
			return 0
		x = self.vectorizer.transform(text)
		pred = self.classifier.predict(x)
		# print(pred.tolist())
		return pred.tolist()
1
# Метод ака main. Берем джейсон с твитами, фигачим его в анализатор, получаем тональности, пишем в словарь
def get_sentiment(person, count):
	sentiments = dict()

	analyzer = SentimentAnalyzer()
	training_corpus = json.load(open(os.path.join(BASE_DIR ,'algorythm/tweets.json')))
	analyzer.train(training_corpus)
	informator.getPerson(person, count)
	person_corpus = json.load(open('_data.json'))
	result = analyzer.getClasses(person_corpus)
	print(result)
	print('COUNT')
	if result != 0:
		positive = result.count(2)/len(person_corpus)
		neutral = result.count(1)/len(person_corpus)
		negative = result.count(0)/len(person_corpus)
		sentiments["positive"] = positive
		sentiments["neutral"] = neutral
		sentiments["negative"] = negative


		for key in sentiments.keys():
			print (key + ": " + str(sentiments.get(key)))

		return sentiments

	else:
		sentiments["positive"] = 0
		sentiments["neutral"] = 0
		sentiments["negative"] = 0


		for key in sentiments.keys():
			print (key + ": " + str(sentiments.get(key)))

		return sentiments

