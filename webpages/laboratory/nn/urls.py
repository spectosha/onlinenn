from django.urls import path
from . import views

urlpatterns = [
	path('<int:nn_id>/', views.nnedit, name='nn'),
	path('<int:nn_id>/<str:start>/', views.start_training, name='nn_start'),
	path('creating/<int:nn_id>/', views.model_creating, name='model_creating'),
    path('creating/<int:nn_id>/redirect/', views.model_adding, name='model_adding'),
	path('delete/<int:nn_id>/redirect/', views.delete, name='delete'),
	path('stop_training/<int:nn_id>/', views.stop_training, name='stop_training'),
	path('get_progress/<int:nn_id>/', views.get_progress, name='get_progress'),
	path('download_keras_model/<int:nn_id>/', views.download_keras_model, name='download_keras_model'),
	path('download_numpy_weigths/<int:nn_id>/', views.download_numpy_weigths, name='download_numpy_weigths'),
]