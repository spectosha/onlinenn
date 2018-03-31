from django.shortcuts import render
from webpages.laboratory.nn.models import NN
def laboratory_learning(request):
	nn_list = NN.objects.filter(id_user=request.user,complite=False)

	return render(request, 'laboratory/Laboratory.html', {'pagename': 'Laboratory',
														  'subpage':'Now',
														  'nn_list':nn_list})

def laboratory_ended(request):
	nn_list = NN.objects.filter(id_user=request.user,complite=True)

	return render(request, 'laboratory/Laboratory.html', {'pagename': 'Laboratory',
														  'subpage':'Ended',
														  'nn_list': nn_list})