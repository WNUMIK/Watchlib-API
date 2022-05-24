from rest_framework import status, filters, generics, viewsets, exceptions, response, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from watch.api import serializers, pagination, permissions, throttling
from watch.models import WatchList, StreamPlatform, Review


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    throttle_classes = [throttling.ReviewCreateThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise exceptions.ValidationError('You have already reviewed this!')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    serializer_class = serializers.ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class StreamPlatformAV(views.APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platform, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(views.APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return response.Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(platform)
        return response.Response(serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return response.Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return response.Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    pagination_class = pagination.WatchListCPagination

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    filter_backends = [filters.SearchFilter]
    search_fields = ['=title', 'platform__name']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating']


class WatchListAV(views.APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        items = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(items, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(views.APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return response.Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchListSerializer(item)
        return response.Response(serializer.data)

    def put(self, request, pk):
        try:
            item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return response.Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchListSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return response.Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
