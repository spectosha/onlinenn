from django.shortcuts import render
from webpages.laboratory.nn.models import NN

def cabinet(request):
	return render(request, 'cabinet/Cabinet.html', {'pagename': 'Profile',
													'subpage': 'Research',
													})

def cabinet_nn(request):
	nn_learning = NN.objects.filter(id_user=request.user,complite=False)
	nn_ended = NN.objects.filter(id_user=request.user,complite=True)

	return render(request, 'cabinet/Cabinet.html', {'pagename': 'Profile',
													'subpage': 'CabinetNN',
													'nn_learning': nn_learning,
													'nn_ended': nn_ended
													})

def settings(request):
	return render(request, 'cabinet/Cabinet.html', {'pagename': 'Settings',
													'subpage': 'Contacts',
													})

def settings_sequrity(request):
	return render(request, 'cabinet/Cabinet.html', {'pagename': 'Settings',
													'subpage': 'Sequrity',
													})