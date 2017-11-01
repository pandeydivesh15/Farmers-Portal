# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from location.models import Location
from User.models import Farmer

# Create your models here.
class Crop(models.Model):
	"""docstring for Crop"""
	crop_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length = 40)
	family = models.CharField(max_length = 40)

	def __unicode__(self):
		return self.name + ", " + self.family
	def __str__(self):
		return self.name + ", " + self.family

class Nutrient(models.Model):
	"""docstring for Nutrient"""
	nut_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length = 40)
	nut_type = models.CharField(max_length = 40)

	def __unicode__(self):
		return self.name + ", " + self.nut_type
	def __str__(self):
		return self.name + ", " + self.nut_type

class Disease(models.Model):
	"""docstring for Disease"""
	dis_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length = 40)
	category = models.CharField(max_length = 50)
	image = models.FileField(null=True, blank=True, upload_to='diseases/'	)

	def __unicode__(self):
		return self.name + ", " + self.category
	def __str__(self):
		return self.name + ", " + self.category

class Fertilizer(models.Model):
	"""docstring for Fertilizer"""
	ferti_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length = 40)

	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

# Tables for many to many relationships
class SoilNutrient(models.Model):
	"""docstring for SoilNutrient"""
	class Meta:
		unique_together = (('location', 'nutrient'),)

	location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
	nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, blank=True, null=True)

	def __unicode__(self):
		return unicode(self.location) + '---->' + self.nutrient.name
	def __str__(self):
		return unicode(self.location) + '---->' + self.nutrient.name

class FertiProvide(models.Model):
	"""docstring for FertiProvide"""
	class Meta:
		unique_together = (('ferti', 'nutrient'),)

	ferti = models.ForeignKey(Fertilizer, on_delete=models.CASCADE, blank=True, null=True)
	nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, blank=True, null=True)

	def __unicode__(self):
		return self.ferti.name + ', ' + self.nutrient.name
	def __str__(self):
		return self.ferti.name + ', ' + self.nutrient.name

class CropNutrient(models.Model):
	"""docstring for CropNutrient"""
	class Meta:
		unique_together = (('crop', 'nutrient'),)

	crop = models.ForeignKey(Crop, on_delete=models.CASCADE, blank=True, null=True)
	nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, blank=True, null=True)

	def __unicode__(self):
		return self.crop.name + ', ' + self.nutrient.name
	def __str__(self):
		return self.crop.name + ', ' + self.nutrient.name


class CropFarmer(models.Model):
	"""docstring for CropFarmer"""
	class Meta:
		unique_together = (('crop', 'disease', 'farmer'),)

	crop = models.ForeignKey(Crop, on_delete=models.CASCADE, blank=True, null=True)
	disease = models.ForeignKey(Disease, on_delete=models.CASCADE, blank=True, null=True)
	farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, blank=True, null=True)
	remark = models.CharField(max_length = 200, blank=True, null=True)

	def __unicode__(self):
		return self.crop.name + ', ' + self.farmer.name
	def __str__(self):
		return self.crop.name + ', ' + self.farmer.name