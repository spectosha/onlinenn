from django import forms

class NnEditForm(forms.Form):
	name = forms.CharField(required=None, label="Give the model a name or change it.", max_length=120, widget=forms.TextInput(attrs={'placeholder': '',
																						'class': 'form-control-w margin-0'}))
	samples = forms.FileField(required=None, label="Load your training samples", help_text="", widget=forms.TextInput(attrs={'type': 'file',
																					'class': 'margin-10'}))

	def clean(self, *args, **kwargs):
		name = self.cleaned_data.get('name')
		samples = self.cleaned_data.get('samples')
		if name == '' and samples is None:
			forms.ValidationError('Error: Fill the fields')

		return super(NnEditForm, self).clean(*args, **kwargs)

	def is_valid(self):
		valid = super(forms.Form, self).is_valid()

		name = self.cleaned_data['name']
		samples = self.cleaned_data['samples']

		#if name == '' and samples is None:
		#	return False
		return True

class ModelEditForm(forms.Form):
	mySavedModel = forms.CharField(required=None)

	def clean(self, *args, **kwargs):
		mySavedModel = self.cleaned_data.get('mySavedModel')
		if mySavedModel == '':
			forms.ValidationError('Error: Fill the fields')

		return super(ModelEditForm, self).clean(*args, **kwargs)

