# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Expert
from .models import Farmer

class FarmerModelAdmin(admin.ModelAdmin):
	"""docstring for PostModelAdmin"""
	class Meta:
		model = Farmer
	list_display=["__unicode__", "join_timestamp"]
	list_display_links=["__unicode__"]
	list_filter= ["join_timestamp"]
	search_fields =["name"]

class ExpertModelAdmin(admin.ModelAdmin):
	"""docstring for PostModelAdmin"""
	class Meta:
		model = Expert
	list_display=["__unicode__", "join_timestamp"]
	list_display_links=["__unicode__"]
	list_filter= ["join_timestamp"]
	search_fields =["name"]

# admin.site.register(Expert, ExpertModelAdmin)
# admin.site.register(Farmer, FarmerModelAdmin)