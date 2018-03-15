from django.shortcuts import render

def signup(request):
	return render(request, 'signup/Sign up.html', {'pagename':'Sign up'})