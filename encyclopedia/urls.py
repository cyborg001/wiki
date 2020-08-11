from django.urls import path

from . import views

<<<<<<< HEAD
app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("entry", views.entry, name="entry"),
=======

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
>>>>>>> entry_feature
]
