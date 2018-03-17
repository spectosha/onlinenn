from django.shortcuts import render

# Create your views here.
def how_to_start(request):
	return render(request, 'how_to_start/How to start.html', {'pagename':'How to start'})
