from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='stream-platform')

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', views.WatchDetailAV.as_view(), name='watch-detail'),

    path('', include(router.urls)),
    # path('stream/', views.StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', views.StreamPlatformDetailAV.as_view(), name='stream-detail'),

    path('stream/<int:pk>/review-create', views.ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review', views.ReviewList.as_view(), name='stream-detail'),
    path('stream/review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),
]