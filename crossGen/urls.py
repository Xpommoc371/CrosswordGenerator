from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('view_json', views.view_jsons, name="view_json")
]