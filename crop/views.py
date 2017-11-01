from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.db import connection, transaction

# Create your views here.
from User.models import check_if_auth_user

from collections import namedtuple

def namedtuplefetchall(cursor):
	"Return all rows from a cursor as a namedtuple"
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]

def register_crop(request):
	check = check_if_auth_user(request)
	current_user = None
	user_class = None
	if check:
		cursor = connection.cursor()
		user_class = request.session["user_class"]
		if user_class == 'E':
			query = "SELECT * FROM User_expert WHERE `User_expert`.'user_id' = %s"
		else:
			query = "SELECT * FROM User_farmer WHERE `User_farmer`.'user_id' = %s"

		cursor.execute(query, [check, ])
		result = namedtuplefetchall(cursor)
		current_user = result[0]

	if current_user is None:
		messages.error(request, "Perform Login first")
		return redirect("home:welcome")
	if user_class == 'E':
		messages.error(request, "Sorry, but only farmers are allowed to register their crops.")
		return redirect("home:welcome")

	query = "SELECT crop_id, name FROM crop_crop";
	cursor.execute(query, [])
	result = namedtuplefetchall(cursor)
	all_crops_dict = {x.name:x.crop_id for x in result}
	all_crop_names = [x.name for x in result]

	if request.method == "POST":
		name = request.POST.get('crop_name')
		remark = request.POST.get('crop_remark')

		cursor = connection.cursor()

		query = "SELECT * FROM crop_cropfarmer WHERE `crop_cropfarmer`.'crop_id' = %s and `crop_cropfarmer`.'farmer_id' = %s"
		cursor.execute(query, [all_crops_dict[name], current_user.auto_id])
		result = namedtuplefetchall(cursor)

		if result:
			messages.error(request,"You have already registered this crop. Delete previous and re-register")
			return redirect("crop:register")

		# Data modifying operation - commit required
		
		query = "INSERT INTO crop_cropfarmer('crop_id', 'farmer_id', 'remark') Values(%s, %s, %s)"

		
		cursor.execute(query, [all_crops_dict[name], current_user.auto_id, remark])			
		transaction.commit()

		messages.success(request, "Crop succesfully registered.")
		return redirect("crop:detail")

	context_data={
		"crop_names" : all_crop_names,
	}
	return render(request,"register_crop.html",context_data)

def view_crops(request):
	check = check_if_auth_user(request)
	current_user = None
	user_class = None
	if check:
		cursor = connection.cursor()
		user_class = request.session["user_class"]
		if user_class == 'E':
			query = "SELECT * FROM User_expert WHERE `User_expert`.'user_id' = %s"
		else:
			query = "SELECT * FROM User_farmer WHERE `User_farmer`.'user_id' = %s"

		cursor.execute(query, [check, ])
		result = namedtuplefetchall(cursor)
		current_user = result[0]

	if current_user is None:
		messages.error(request, "Perform Login first")
		return redirect("home:welcome")

	if user_class == 'E':
		messages.error(request, "Sorry, but only farmers are allowed here.")
		return redirect("home:welcome")

	query = """
			SELECT  `crop_cropfarmer`.'crop_id', `crop_cropfarmer`.remark, 
					`crop_crop`.name as crop_name, `crop_crop`.family,
					`crop_disease`.name as dis_name, `crop_disease`.category
			FROM crop_cropfarmer
			INNER JOIN `crop_crop` ON `crop_cropfarmer`.'crop_id' = `crop_crop`.'crop_id'
			LEFT JOIN `crop_disease` ON `crop_cropfarmer`.'disease_id' = `crop_disease`.'dis_id'
			WHERE `crop_cropfarmer`.'farmer_id' = %s
			"""
	cursor.execute(query, [current_user.auto_id, ])
	result = namedtuplefetchall(cursor)
	
	context_data={
		"crop_objects_and_diseases" : result,
	}
	return render(request, "view_crops.html", context_data)


def crop_delete(request, id=None):
	check = check_if_auth_user(request)
	current_user = None
	user_class = None
	if check:
		cursor = connection.cursor()
		user_class = request.session["user_class"]
		if user_class == 'E':
			query = "SELECT * FROM User_expert WHERE `User_expert`.'user_id' = %s"
		else:
			query = "SELECT * FROM User_farmer WHERE `User_farmer`.'user_id' = %s"

		cursor.execute(query, [check, ])
		result = namedtuplefetchall(cursor)
		current_user = result[0]

	if current_user is None:
		messages.error(request, "Perform Login first")
		return redirect("home:welcome")

	if user_class == 'E':
		messages.error(request, "Sorry, but only farmers are allowed to delete their crops.")
		return redirect("home:welcome")

	cursor = connection.cursor()
	query = "SELECT * FROM crop_cropfarmer WHERE `crop_cropfarmer`.'crop_id' = %s and `crop_cropfarmer`.'farmer_id' = %s"
	cursor.execute(query, [id, current_user.auto_id])
	result = namedtuplefetchall(cursor)

	if not result:
		messages.error(request,"Given crop was not found")
		return redirect("home:welcome")

	instance = result[0]

	# Data modifying operation - commit required
	query = "DELETE from crop_cropfarmer WHERE `crop_cropfarmer`.'crop_id' = %s and `crop_cropfarmer`.'farmer_id' = %s"
	cursor.execute(query, [id, current_user.auto_id])
	transaction.commit()

	messages.success(request,"Your crop was successfully deleted")
	return redirect("crop:detail")

def tag_disease(request, id=None, crop_id=None):
	check = check_if_auth_user(request)
	current_user = None
	user_class = None
	if check:
		cursor = connection.cursor()
		user_class = request.session["user_class"]
		if user_class == 'E':
			query = "SELECT * FROM User_expert WHERE `User_expert`.'user_id' = %s"
		else:
			query = "SELECT * FROM User_farmer WHERE `User_farmer`.'user_id' = %s"

		cursor.execute(query, [check, ])
		result = namedtuplefetchall(cursor)
		current_user = result[0]

	if current_user is None:
		messages.error(request, "Perform Login first")
		return redirect("home:welcome")

	if user_class == 'F':
		messages.error(request, "Sorry, but only experts are allowed to tag diseases.")
		return redirect("home:welcome")

	query = """
			SELECT  `crop_cropfarmer`.'crop_id', `crop_cropfarmer`.farmer_id, 
					`crop_crop`.name as crop_name, `crop_crop`.family,
					`crop_disease`.name as dis_name, `crop_disease`.category
			FROM crop_cropfarmer
			INNER JOIN `crop_crop` ON `crop_cropfarmer`.'crop_id' = `crop_crop`.'crop_id'
			LEFT JOIN `crop_disease` ON `crop_cropfarmer`.'disease_id' = `crop_disease`.'dis_id'
			WHERE `crop_cropfarmer`.'farmer_id' = %s
			"""
	cursor.execute(query, [id, ])
	crops_and_diseases = namedtuplefetchall(cursor)


	query = """
			SELECT  dis_id, name
			FROM crop_disease
			"""
	cursor.execute(query, [])
	result = namedtuplefetchall(cursor)
	disease_map = {x.name : x.dis_id for x in result}

	if request.method == "POST":
		disease_name = request.POST.get('disease_name')
		print "sda"
		if disease_name:
			cursor = connection.cursor()
			# Data modifying operation - commit required			

			if disease_map.has_key(disease_name):
				query = """
						UPDATE crop_cropfarmer SET disease_id = %s
						WHERE `crop_cropfarmer`.'farmer_id' = %s and `crop_cropfarmer`.'crop_id' == %s"""
				cursor.execute(query, [disease_map[disease_name], id, crop_id])
			else:
				query = """
						UPDATE crop_cropfarmer SET disease_id = NULL
						WHERE `crop_cropfarmer`.'farmer_id' = %s and `crop_cropfarmer`.'crop_id' == %s"""
				cursor.execute(query, [id, crop_id])
			transaction.commit()

		messages.success(request, "Successfully updated the disease tag.")
		return redirect(reverse("crop:disease", kwargs={ "id":id}))


	context_data={
		"crop_objects_and_diseases" : crops_and_diseases,
		"user_class": user_class,
		"disease_names": disease_map.keys(),
	}
	return render(request, "view_crops.html", context_data)



