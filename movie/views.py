from django.shortcuts import render
from django.views import View
from .models import Movie
from django.http import JsonResponse


class MovieList(View):
    def get(self, request):
        movies = Movie.objects.all()
        data = {
            'movies': list(movies.values())
        }

        return JsonResponse(data)