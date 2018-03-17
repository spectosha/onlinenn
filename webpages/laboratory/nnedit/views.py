from django.shortcuts import render

def nnedit(request):
	return render(request, 'nnedit/NN Edit.html', {'pagename':'...'})