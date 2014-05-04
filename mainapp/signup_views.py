from classes.Tags import Tags
from django.shortcuts import render_to_response
# from allauth.socialaccount import views as signup_views
from django.template.response import TemplateResponse
from mainapp import new_signup as signup_views
from mainapp import signup_view as aa_signup

def signup_view(request):
	response = signup_views.signup(request)
	return response

def signup_view_new(request):
	response = aa_signup.signup(request)
	return response
# def my_render_callback(response):
# 	tags = Tags()
# 	parameters={}
# 	all_tags = tags.get_tags()
# 	parameters['all_tags'] = all_tags
# 	return render_to_response('socialaccount/signup.html', parameters)
# 	# return TemplateResponse('socialaccount/signup.html', {'all_tags': all_tags})