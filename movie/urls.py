from django.urls import path
from .views import MovieList

urlpatterns = [
    path('list/', MovieList.as_view(), name='movie-list'),
]