from django.contrib.auth.forms import UserCreationForm

from kitchen_core.models import Cook, DishType


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "years_of_experience"
        )


# class DishTypeDetailForm(forms.ModelForm):
#     dish = forms.ModelMultipleChoiceField(
#         queryset=get_dish_type_model().objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#     )
#
#     class Meta:
#         model = DishType
#         fields = "__all__"
