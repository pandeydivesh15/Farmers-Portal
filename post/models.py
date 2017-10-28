# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

from User.models import Farmer, Expert

POST_CATEGORIES = {
	1: "Crop Disease/Problems",
	2: "Climate Related",
	3: "Others",
}

# Create your models here.
class Post(models.Model):
	"""docstring for Posts"""
	post_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length = 120)
	description = models.TextField()
	category = models.CharField(max_length = 100)

	author_expert = models.ForeignKey(Expert, on_delete=models.CASCADE, blank=True, null=True)
	author_farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, blank=True, null=True)
	# Here, as the post can have only one author, one of the above two values will remain NULL

	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	
	image = models.FileField(null=True, blank=True)

	# image = models.ImageField(
	# 	upload_to = upload_loc,
	# 	null = True, blank = True,
	# 	width_field = "width_field",
	# 	height_field = "height_field")
	# width_field = models.IntegerField(default = 0)
	# height_field = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.title
	def __str__(self):
		return self.title

	def get_absolute_URL(self):
		return reverse("post:detail", kwargs={ "id":self.post_id})

	class Meta:
		ordering = [ "-timestamp", "-updated" ]

class Comment(models.Model):
	"""docstring for Posts"""
	cmnt_id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	text = models.TextField()

	author_expert = models.ForeignKey(Expert, on_delete=models.CASCADE, blank=True, null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

	def __unicode__(self):
		return self.text
	def __str__(self):
		return self.text