from django.urls import re_path
from .views import ListView

"""
URL pattern for the ListView with a dynamic path and optional group parameter.

This pattern captures a path and an optional group from the URL, passing them as
arguments to the ListView view. The path is required, while the group is optional
and can be omitted from the URL.
"""

urlpatterns = [
    re_path(r'^(?P<path>[^?]*)\??(?P<group>.*)$', ListView.as_view(), name='list_view')
]
