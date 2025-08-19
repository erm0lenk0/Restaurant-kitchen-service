from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.views import generic
from .forms import CookCreationForm, DishSearchForm, DishTypeSearchForm, CookSearchForm

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
    paginate_by = 10
    template_name = "kitchen_core/dish_type_list.html"

    def get_context_data(self, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data['name'])
        return queryset





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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


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
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        cook = self.request.GET.get("cook", "")
        context["search_form"] = CookSearchForm(
            initial={"cook": cook},
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            cook_query = form.cleaned_data.get("cook", "")
            queryset = queryset.filter(
                Q(first_name__icontains=cook_query) |
                Q(last_name__icontains=cook_query)
            )
        return queryset

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
