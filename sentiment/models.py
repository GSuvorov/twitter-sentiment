from django.db import models

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=25)
	negative_polarity = models.FloatField(default=0.0)
	positive_polarity = models.FloatField(default=0.0)
	neutral_polarity = models.FloatField(default=0.0)

class Selections(models.Model):
	tweet = models.CharField(max_length=140)
	tweet_polarity = models.CharField(max_length=10)
	person_id = models.ForeignKey(Person, related_name="person_id", default=0)
