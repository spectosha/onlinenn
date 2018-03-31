from django.urls import path
from . import views

urlpatterns = [
	path('<int:nn_id>/', views.nnedit, name='nn'),
	path('<int:nn_id>/<str:start>/', views.start_training, name='nn_start')
]