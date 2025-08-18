from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.views import generic
from .forms import CookCreationForm

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
    queryset = DishType.objects.all()
    # paginate_by = 5


class DishTypeCreateView(generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen_core:dish-type-list")
    template_name = "kitchen_core/dish_type_form.html"


class DishTypeUpdateView(generic.UpdateView):
     model = DishType
     fields = "__all__"
     template_name = "kitchen_core/dish_type_form.html"
     success_url = reverse_lazy("kitchen_core:dish-type-list")


class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    template_name = "kitchen_core/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen_core:dish-type-list")


class DishTypeDetailView(generic.DetailView):
    model = DishType
    template_name = "kitchen_core/dish_type_detail.html"
    context_object_name = "dish_type"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dishes"] = self.object.dishes.all()

        return context


class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen_core/dish_list.html"
    queryset = Dish.objects.select_related("dish_type")
    # paginate_by = 5


class DishCreateView(generic.CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen_core:dish-list")


class DishUpdateView(generic.UpdateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen_core:dish-list")


class DishDeleteView(generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen_core:dish-list")


class DishDetailView(generic.DetailView):
    model = Dish

class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "kitchen_core/cook_list.html"
    queryset = Cook.objects.all()
    # paginate_by = 5


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen_core:cook-list")


class CookUpdateView(generic.UpdateView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("kitchen_core:cook-list")


class CookDeleteView(generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen_core:cook-list")


class CookDetailView(generic.DetailView):
    model = Cook
