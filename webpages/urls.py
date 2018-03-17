
from django.urls import path, include

urlpatterns = [
    path('', include('webpages.index.urls')),
    path('how_to_start/', include('webpages.how_to_start.urls')),
    path('signup/', include('webpages.signup.urls')),
    path('login/', include('webpages.login.urls')),
    path('cabinet/', include('webpages.cabinet.urls')),
    path('laboratory/', include('webpages.laboratory.urls')),
]