from django.shortcuts import render
from django.contrib.auth.models import User

def signup(request):
	return render(request, 'signup/Sign up.html', {'pagename':'Sign up'})
