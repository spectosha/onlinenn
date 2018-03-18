from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Username',
																					 'class':'form-control'}))
	password = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Password',
																					 'class':'form-control',
																					 'type':'password'}))

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError('Error: This user does not exist')
			if not user.check_password(password):
				raise forms.ValidationError('Error: Incorrect password')
			if not user.is_active:
				raise forms.ValidationError('Error: This user is not longer active')
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	username = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Username',
																					 'class': 'form-control'}))
	email = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'E-mail',
																					 'class': 'form-control'}))
	password = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Password',
																					 'class': 'form-control',
																					 'type': 'password'}))
	password2 = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Password again',
																					 'class': 'form-control',
																					 'type': 'password'}))
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
		]

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		username = User.objects.filter(email=username)
		email_qs = User.objects.filter(email=email)
		if username.exists():
			raise forms.ValidationError('This username has already been registered')
		if email_qs.exists():
			raise forms.ValidationError('This email has already been registered')
		if password != password2:
			raise forms.ValidationError('Passwords must match')
		if len(password)<8:
			raise forms.ValidationError('Password must contain at least 8 characters')
		return super(UserRegisterForm,self).clean(*args, **kwargs)

	#def clean_email(self, *args, **kwargs):
	#	email = self.cleaned_data.get('email')
	#	email_qs = User.objects.filter(email=email)
	#	if email_qs.exists():
	#		raise forms.ValidationError('This email has already been registered')
	#	return email



