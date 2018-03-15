from django.shortcuts import render

def login(request):
	return render(request, 'login/Log in.html', {'pagename':'Log in'})