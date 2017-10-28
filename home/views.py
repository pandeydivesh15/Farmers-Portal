from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count
from django.db import connection, transaction

from post.models import POST_CATEGORIES
from User.models import check_if_auth_user

from collections import namedtuple

def namedtuplefetchall(cursor):
	"Return all rows from a cursor as a namedtuple"
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]

# Create your views here.
def index_page(request):	
	check = check_if_auth_user(request)
	current_user = None
	if check:
		cursor = connection.cursor()
		if request.session["user_class"] == 'E':
			query = "SELECT * FROM User_expert WHERE `User_expert`.'user_id' = %s"
		else:
			query = "SELECT * FROM User_farmer WHERE `User_farmer`.'user_id' = %s"

		cursor.execute(query, [check, ])
		result = namedtuplefetchall(cursor)
		current_user = result[0]

	cursor = connection.cursor()
	cursor.execute("SELECT * FROM post_post ORDER BY `post_post`.'timestamp' desc")
	result = namedtuplefetchall(cursor)
	context_data = {
		"all_posts" : result,
		"user" : current_user,
	}

	return render(request, "index.html" , context_data)