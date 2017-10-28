# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Post, Comment

class PostModelAdmin(admin.ModelAdmin):
	"""docstring for PostModelAdmin"""
	class Meta:
		model = Post
	list_display=["title", "author_expert", "author_farmer"]
	list_display_links=["title"]
	list_filter= ["timestamp"]
	search_fields =["title", "author_expert__name", "author_farmer__name"]

class CommentModelAdmin(admin.ModelAdmin):
	"""docstring for PostModelAdmin"""
	class Meta:
		model = Comment

admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)