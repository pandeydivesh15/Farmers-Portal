from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
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

# Defining queries for the index page
QUERY_DICT = {
	1 : """
		SELECT name as Name, user_id as Email FROM User_farmer 
		WHERE `User_farmer`.'name' LIKE %s or `User_farmer`.'location_id' in 
			(SELECT `location_location`.loc_id FROM location_location 
			WHERE `location_location`.city LIKE %s or `location_location`.state LIKE %s)""",

	2 : """
		SELECT title as Title, timestamp as PostedOn, post_id as Link FROM post_post 
		WHERE `post_post`.'title' LIKE %s or 
		`post_post`.'description' LIKE %s or `post_post`.'post_id' = %s""",

	3 : """
		SELECT name as CropName, family as Family FROM crop_crop 
		WHERE `crop_crop`.'name' LIKE %s or 
		`crop_crop`.'family' LIKE %s or `crop_crop`.'crop_id' = %s""",

	4 : """
		SELECT name as Name, user_id as Email FROM User_farmer 
		WHERE `User_farmer`.'location_id' = %s""",

	5 : """
		SELECT `crop_crop`.name as CropName, `crop_crop`.family as Family,
				`User_farmer`.name as FarmerName, `User_farmer`.'user_id' as Email, 
				`crop_disease`.name as Disease, `crop_disease`.category as Category
		FROM crop_crop 
		INNER JOIN `crop_cropfarmer` ON `crop_cropfarmer`.'crop_id' = `crop_crop`.'crop_id'
		INNER JOIN `User_farmer` ON `User_farmer`.'auto_id' = `crop_cropfarmer`.'farmer_id'
		INNER JOIN `crop_disease` ON `crop_disease`.'dis_id' = `crop_cropfarmer`.'disease_id'
		""",

	6 : """
		SELECT `crop_fertilizer`.'name' as Fertilizer, `crop_nutrient`.'name' as Nutrient, `crop_nutrient`.'nut_type' as NutrientType 
		FROM crop_fertiprovide
		INNER JOIN crop_nutrient ON `crop_fertiprovide`.nutrient_id = `crop_nutrient`.'nut_id'
		INNER JOIN crop_fertilizer ON `crop_fertiprovide`.ferti_id = `crop_fertilizer`.'ferti_id'
		ORDER BY Fertilizer""",
}

# Create your views here.
def index_page(request):	
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

	cursor = connection.cursor()
	cursor.execute("SELECT * FROM post_post ORDER BY `post_post`.'timestamp' desc")
	result = namedtuplefetchall(cursor)
	context_data = {
		"all_posts" : result,
		"user" : current_user,
		"user_class": user_class,
	}

	return render(request, "index.html" , context_data)

def query_resolve(request, id=None):
	if not QUERY_DICT.has_key(int(id)):
		messages.error(request, "Wrong query given. Please try again.")
		return redirect("home:welcome") 

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

	if not current_user:
		messages.error(request, "Please login first.")
		return redirect("home:welcome")

	result = None
	result_header = None
	result_farmers = None

	if int(id) > 3:
		if user_class == 'F':
			messages.error(request, "Only experts allowed for these queries.")
			return redirect("home:welcome")

		query = QUERY_DICT[int(id)]
		if int(id) == 4:
			query = query % current_user.location_id
		cursor.execute(query)
		result = namedtuplefetchall(cursor)		
		result_header = [col[0] for col in cursor.description]

	context_data = {
		"user" : current_user,
		"user_class": user_class,
		"query_id": id,
		"result_header": result_header,
		"result": result,
		"result_farmers": result_farmers,

	}
	return render(request, "query.html" , context_data)

def search_database(request, id):
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

	if not current_user:
		messages.error(request, "Please login first.")
		return redirect("home:welcome")

	if int(id) > 3:
		messages.error(request, "This is not a searchable query. Redirecting.")
		return redirect(reverse("home:query", kwargs={"id":id}))

	search_query = request.GET.get('search_query')

	if not search_query:
		messages.error(request, "Enter a suitable query. Try again")
		return redirect(reverse("home:query", kwargs={"id":id}))

	search_query += '%'
	# '%' because it will search for a pattern using LIKE op

	cursor.execute(QUERY_DICT[int(id)], [search_query, search_query, search_query])
	result = namedtuplefetchall(cursor)
	result_header = [col[0] for col in cursor.description]

	if not result:
		messages.error(request, "No records match. Try again")

	result_farmers = []
	if int(id) == 3:
		query = "SELECT * FROM User_farmer"
		cursor.execute(query, [])
		result_farmers = namedtuplefetchall(cursor)

	context_data = {
		"user" : current_user,
		"user_class": user_class,
		"query_id": id,
		"result_header": result_header,
		"result": result,
		"result_farmers": result_farmers,
	}
	return render(request, "query.html" , context_data)

def get_faq(request):
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
	context_data = {
		"user" : current_user,
	}
	return render(request, "faq.html" , context_data)

def about_us(request):
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
	context_data = {
		"user" : current_user,
	}
	return render(request, "aboutus.html" , context_data)