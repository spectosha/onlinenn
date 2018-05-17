from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import NN
from django.http import Http404
from .forms import NnEditForm, ModelEditForm
from .tasks import train
from django.views.decorators.csrf import csrf_exempt

def nnedit(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")

	form = NnEditForm(request.POST, request.FILES)
	if form.is_valid():
		if form.cleaned_data.get('name') != '':
			nn.name = form.cleaned_data.get('name')
			nn.save()
		if(request.FILES.__len__() != 0):
			nn.samples.save(nn.name, request.FILES['samples'], True)
			nn.save(update_fields=['samples'])
	new = False
	try:
		nn.weights.url
		nn.model.url
	except:
		new = True

	return render(request, 'nnedit/NN Edit.html', {'pagename': nn.name, 'nn': nn, 'new': new, 'form': form})

def start_training(request, nn_id, start):
	if start == 'True':
		train.delay(request.user, nn_id)
	return redirect('/laboratory/nn/' + str(nn_id) + '/')

def model_creating(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")

	form = ModelEditForm(request.POST)

	model = nn.model_json
	return render(request, 'model_creating/model_creating.html', {'pagename': nn.name, 'nn': nn, 'model': model, "form": form})


def model_adding(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")

	form = ModelEditForm(request.POST)
	if form.is_valid():
		nn.model_json = form.cleaned_data.get('mySavedModel')
		model = nn.model_json
		nn.save()

		return redirect('/laboratory/nn/' + str(nn_id) + '/')

	return redirect('/laboratory/nn/creating/' + str(nn_id) + '/')

def stop_training(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")
	nn.complite = True
	nn.save()
	print(nn.complite)
	return redirect('/laboratory/nn/' + str(nn_id) + '/')

@csrf_exempt
def get_progress(request, nn_id):
	if request.method != "POST":
		return

	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")

	return JsonResponse({'progress': str(nn.progress), 'loosing': str(nn.loosing)})

def download_keras_model(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")
	myfile = nn.model
	fs = FileSystemStorage()
	filename = fs.save(myfile.name, myfile)
	uploaded_file_url = fs.url(filename)
	print(uploaded_file_url)
	return uploaded_file_url

def download_numpy_weigths(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")

	return nn.weights

def delete(request, nn_id):
	try:
		nn = NN.objects.get(id=nn_id)
	except NN.DoesNotExist:
		raise Http404("Neural network does not exist")
	if nn.id_user != request.user:
		raise Http404("Page not found")
	nn.delete()
	return redirect('/laboratory/')