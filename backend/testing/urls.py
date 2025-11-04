from django.urls import path
from . import views

app_name = "testing"

urlpatterns = [
    path("ping/", views.ping, name="ping"),   # GET
    path("echo/", views.echo, name="echo"),   # POST
    path("db/", views.db_test, name="db_test"),  # GET
]
