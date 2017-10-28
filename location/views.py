# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.db import connection, transaction

from User.models import check_if_auth_user

from collections import namedtuple

def namedtuplefetchall(cursor):
	"Return all rows from a cursor as a namedtuple"
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]

# Create your views here.

def weather_query(request, id):
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

	if current_user is None:
		messages.error(request, "Perform Login first")
		return redirect("home:welcome")

	if request.session["user_class"] == 'F':
		messages.error(request, "Sorry, only experts are allowed to study location's weather.")
		return redirect("home:welcome")

	query = "SELECT * FROM location_location WHERE `location_location`.loc_id = %s"
	cursor.execute(query, [id, ])
	result = namedtuplefetchall(cursor)

	if not result:
		messages.error(request, "Such location doesn't exist.")
		return redirect("home:welcome")

	location = result[0]

	query = "SELECT * FROM location_weather WHERE `location_weather`.'location_id' = %s ORDER BY `location_weather`.'date_record' DESC"
	cursor.execute(query, [id, ])
	result = namedtuplefetchall(cursor)

	context_data = {
		"user": current_user,
		"location": location,
		"weather_info": result[:10], # Only recent 10 records will be shown
	}
	return render(request, "location.html", context_data)




