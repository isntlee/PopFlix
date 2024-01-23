from django.urls import re_path
from .views import ListView

urlpatterns = [
    re_path(r'^(?P<path>.*)/$', ListView.as_view()),
]