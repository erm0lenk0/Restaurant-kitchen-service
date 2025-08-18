from django.urls import path

from .models import DishType, Cook
from .views import (
    index,
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishTypeDetailView,
    DishListView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    DishDetailView,
    CookListView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    CookDetailView,
)

app_name = "kitchen_core"


urlpatterns = [
    path("", index, name="index"),
    path("dish_type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish_type/create", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish_type/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish_type/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dish_type/<int:pk>/", DishTypeDetailView.as_view(), name="dish-type-detail"),

    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),

    path("cook/", CookListView.as_view(), name="cook-list"),
    path("cook/create/", CookCreateView.as_view(), name="cook-create"),
    path("cook/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cook/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
]
