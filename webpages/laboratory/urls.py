from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.laboratory_learning, name='laboratory_learning'),
	path('ended/', views.laboratory_ended, name='laboratory_ended'),
	path('nnedit/', include('webpages.laboratory.nnedit.urls')),
]