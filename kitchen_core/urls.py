from django.urls import path
from .views import (
    index,
)

app_name = "kitchen_core"


urlpatterns = [
    path("", index, name="index"),
]


