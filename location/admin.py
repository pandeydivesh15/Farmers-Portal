# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Location, Weather

class LocationModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Location
	list_display=["__unicode__"]

class WeatherModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Weather
	list_display=["__unicode__"]

admin.site.register(Location, LocationModelAdmin)
admin.site.register(Weather, WeatherModelAdmin)