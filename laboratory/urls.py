from django.urls import path
from . import views

urlpatterns = [
	path('', views.laboratory_learning, name='laboratory_learning'),
	path('ended/', views.laboratory_ended, name='laboratory_ended')
]