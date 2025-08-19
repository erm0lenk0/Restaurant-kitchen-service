from django.contrib.auth.forms import UserCreationForm

from kitchen_core.models import Cook, DishType
from django import forms


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "years_of_experience"
        )



class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by Name"}),
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by Name"
            }
        )
    )

class CookSearchForm(forms.Form):
    cook = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by First Name or Last Name"
            }
        )
    )