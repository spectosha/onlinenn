from django.urls import path
from . import views

urlpatterns = [
	path('', views.cabinet, name='cabinet'),
	path('nn/',views.cabinet_nn, name='cabinet_nn'),
	path('settings/', views.settings, name='contacts'),
	path('settings/security/', views.settings_sequrity, name='security'),
]