from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import MovieSerializer
from movie.models import Movie


class MovieList(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetail(APIView):
    def get(self, request, pk, format=None):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
