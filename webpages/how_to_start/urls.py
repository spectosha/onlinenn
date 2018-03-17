from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.how_to_start, name="how_to_start"),
]