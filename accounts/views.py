from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user, login, logout
from .forms import UserLoginForm, UserRegisterForm
# Create your views here.
def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('/')
	return render(request, 'login/Log in.html', {'pagename':'Log in',
												 'form':form})

def registration_view(request):
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		return redirect('/')
	return render(request, 'signup/Sign up.html', {'pagename':'Sign up',
												 'form':form})

def logout_view(request):
	form = UserLoginForm(request.POST or None)
	logout(request)
	return redirect('/login/')