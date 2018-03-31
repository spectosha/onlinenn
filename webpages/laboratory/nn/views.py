from django.shortcuts import render, redirect
from .models import NN
from django.http import Http404
from .forms import NnEditForm
from .tasks import train

def nnedit(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")

	form = NnEditForm(request.POST, request.FILES)
	if form.is_valid():
		nn.name = form.cleaned_data.get('name')
		name_samples = str(request.user) + '_' + str(nn.id) + '.npy'
		nn.samples.save(name_samples, request.FILES['samples'], True)

	return render(request, 'nnedit/NN Edit.html', {'pagename': nn.name, 'nn': nn, 'form': form})

def start_training(request, nn_id, start):
	if start == 'True':
		train.delay(nn_id)
	return redirect('/laboratory/nn/' + str(nn_id) + '/')
