from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .algorythm.sentimentAnalyzer import get_sentiment
from .algorythm.informator import get_tweets_list
from .models import Person, Selections

# Create your views here.

def page_index(request):
	context = RequestContext(request,{},)
	template = loader.get_template("sentiment/index.html")

	return HttpResponse(template.render(context))

def page_result(request):
	person_name = request.POST["person"]
	sentiments = get_sentiment(person_name, 100)

	person_positive_polarity = sentiments["positive"]
	person_neutral_polarity = sentiments["neutral"]
	person_negative_polarity = sentiments["negative"]

	Person.objects.create(name=person_name,
		positive_polarity=person_positive_polarity,
		neutral_polarity=person_neutral_polarity,
		negative_polarity=person_negative_polarity,
	)

	context = RequestContext(request,
		{"person_name": person_name, "sentiments": sentiments}
	)
	template = loader.get_template("sentiment/result.html")

	return HttpResponse(template.render(context))

def page_details(request):
	person_name = request.POST["person"]
	tweets = get_tweets_list()
	context = RequestContext(request, 
		{"tweets": tweets}
	)
	template = loader.get_template("sentiment/details.html")

	return HttpResponse(template.render(context))
