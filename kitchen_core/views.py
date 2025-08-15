from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views import generic

from .models import Dish, DishType, Cook


def index(request: HttpRequest) -> HttpResponse:
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()
    num_cooks = Cook.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
        "num_cooks": num_cooks,
        "num_visits": num_visits,
    }
    return render(request, "kitchen_core/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen_core/dish_type_list.html"
    queryset = DishType.objects.prefetch_related("name")
    # paginate_by = 5


class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen_core/dish_list.html"
    queryset = Dish.objects.select_related("dish_type")
    # paginate_by = 5


class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "kitchen_core/cook_list.html"
    queryset = Cook.objects.all()
    # paginate_by = 5
