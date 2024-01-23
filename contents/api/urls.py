from django.urls import path, re_path
from .views import ListView, DetailView

urlpatterns = [
    re_path(r'^(?P<path>.*)/$', ListView.as_view()),
]