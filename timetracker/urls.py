from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from timetracker import views


router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet, base_name='activity')


urlpatterns = [
    url(r'^', include(router.urls)),
]
