from django.urls import path
from .views import ChannelListView, ContentListView

urlpatterns = [
    path('channels/<str:slug>', ChannelListView.as_view()),
    path('contents/<int:pk>', ContentListView.as_view()),
]