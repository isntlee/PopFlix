from django.urls import path
from .views import ChannelListView, ChannelDetailView, ContentListView, ContentDetailView

urlpatterns = [
    path('channels/', ChannelListView.as_view()),
    path('channels/<int:pk>/', ChannelDetailView.as_view()),
    path('contents/', ContentListView.as_view()),
    path('contents/<int:pk>/', ContentDetailView.as_view()),
]