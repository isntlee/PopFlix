from django.urls import re_path
from .views import ListView

#Note: This will all have to be reviewed/studied

urlpatterns = [
    re_path(r'^(?P<path>[^?]*)\??(?P<group>.*)$', ListView.as_view(), name='list_view')
]