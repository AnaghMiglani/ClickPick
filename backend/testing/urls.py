from django.urls import path
from . import views

app_name = "testing"

urlpatterns = [
    path("ping/", views.ping, name="ping"),   # GET
    path("echo/", views.echo, name="echo"),   # POST
    path("csrf/", views.get_csrf, name="get_csrf"),
]
