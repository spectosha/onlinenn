from django.shortcuts import render

def laboratory_learning(request):
	return render(request, 'laboratory/Laboratory.html', {'pagename': 'Laboratory',
														  'subpage':'Now',
														  })

def laboratory_ended(request):
	return render(request, 'laboratory/Laboratory.html', {'pagename': 'Laboratory',
														  'subpage':'Ended',
														  })