from django.conf.urls import url

from timetracker import views


urlpatterns = [
    url(r'^activities/$', views.activity_list_view, name='activity-list'),
]
