from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kitchen_core.models import DishType, Dish, Cook


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience", )
    fieldsets = UserAdmin.fieldsets +   (("Additional info", {"fields": ("years_of_experience",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("years_of_experience",)}),)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_display = ("name", "dish_type", "price", "get_cooks")


    @admin.display(description="Cooks")
    def get_cooks(self, obj):
        return ", ".join([str(cook) for cook in obj.cooks.all()])


admin.site.register(DishType)

