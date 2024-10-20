from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:url>", views.open, name="page"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("wiki/<str:url>/edit", views.edit, name="edit"),
    path("wiki/<str:url>/delete", views.delete, name="delete"),
    path("random", views.random_page, name="random"),
]
