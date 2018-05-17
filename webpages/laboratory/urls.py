from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.laboratory_learning, name='laboratory_learning'),
	path('ended/', views.laboratory_ended, name='laboratory_ended'),
	path('nn/', include('webpages.laboratory.nn.urls')),
	path('create/', views.create_new, name='create_new'),
]