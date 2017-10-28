# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
	loc_id = models.AutoField(primary_key=True)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)

	def __unicode__(self):
		return self.city + ', ' + self.state
	def __str__(self):
		return self.city + ', ' + self.state

class Weather(models.Model):
	wea_id = models.AutoField(primary_key=True)
	temperature = models.IntegerField()
	humidity = models.IntegerField()
	date_record = models.DateField()
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __unicode__(self):
		return str(self.location) + ', ' + str(self.wea_id)
	def __str__(self):
		return str(self.location) + ', ' + str(self.wea_id)