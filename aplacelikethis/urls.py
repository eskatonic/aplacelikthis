from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

# Use app_name to organize URLs by application. Here we have only one at the moment.
# Best practice is to have a separate urls.py for each application.
app_name = 'aplacelikethis'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    # path converters:
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_details,
         name='post_details'),
    path('<int:post_id>/share/',
         views.post_share,
         name='post_share'),
]
