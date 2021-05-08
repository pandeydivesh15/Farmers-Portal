# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from location.models import Location

# Create your models here.
class Farmer(models.Model):
	"""docstring for Farmer"""
	auto_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)

	user_id = models.EmailField(max_length=30,unique=True)
	user_pwd = models.CharField(max_length=100)

	contact = models.BigIntegerField()
	
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	join_timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

class Expert(models.Model):
	"""docstring for Farmer"""
	auto_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)

	user_id = models.EmailField(max_length=30,unique=True)
	user_pwd = models.CharField(max_length=30)

	contact = models.BigIntegerField()
	
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	join_timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name
	
def start_user_session(request, user_id, user_class):
	if request.session is not None:
		request.session["user_mail_id"] = user_id
		request.session["user_class"] = user_class
	return request

def check_if_auth_user(request):
	if (request.session is not None) and request.session.has_key("user_mail_id"):
		return request.session["user_mail_id"]
	else:
		return None

def stop_user_session(request):
	if (request.session is not None) and request.session.has_key("user_mail_id"):
		del request.session["user_mail_id"]
		del request.session["user_class"]
		return True
	return False
