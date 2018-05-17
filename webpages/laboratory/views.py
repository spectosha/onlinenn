from django.shortcuts import render, redirect
from webpages.laboratory.nn.models import NN
def laboratory_learning(request):
	nn_list = NN.objects.filter(id_user=request.user, complite=False)

	return render(request, 'laboratory/Laboratory.html', {'pagename': 'Laboratory',
														  'subpage':'Now',
														  'len':len(nn_list)==0,
														  'nn_list':nn_list})

def laboratory_ended(request):
	nn_list = NN.objects.filter(id_user=request.user, complite=True)

	return render(request, 'laboratory/Laboratory.html', {'pagename': 'Laboratory',
														  'subpage':'Ended',
														  'len':len(nn_list)==0,
														  'nn_list': nn_list})

def create_new(request):
	nn = NN(id_user=request.user, complite=True, model_json="{ \"class\": \"go.GraphLinksModel\",  \"nodeDataArray\": [],  \"linkDataArray\": []}")
	nn.save()
	return redirect('/laboratory/nn/' + str(nn.id) + '/')