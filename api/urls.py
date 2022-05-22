from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', views.WatchDetailAV.as_view(), name='watch-detail'),
    path('stream/', views.StreamPlatformAV.as_view(), name='stream-list'),
    path('stream/<int:pk>', views.StreamPlatformDetailAV.as_view(), name='stream-detail'),

    path('review', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),
]