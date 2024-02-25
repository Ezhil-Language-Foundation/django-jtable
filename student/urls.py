from django.urls import path

from . import views

urlpatterns = [
    path("csrf/", views.csrf, name="csrf"),
    path("listAction/", views.listAction, name="listAction"),
    path("updateAction/", views.updateAction, name="updateAction"),
    path("createAction/", views.createAction, name="createAction"),
    path("deleteAction/", views.deleteAction, name="deleteAction"),
]
