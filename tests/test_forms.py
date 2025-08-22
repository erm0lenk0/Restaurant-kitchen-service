from django.test import TestCase
from kitchen_core.forms import (
    CookCreationForm,
    DishSearchForm,
    DishTypeSearchForm,
    CookSearchForm
)

class FormTests(TestCase):

    def test_dish_type_search_form_valid_data(self):
        form_data = {"name": "Pizza"}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_dish_type_search_form_empty_data(self):
        form = DishTypeSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_dish_search_form_valid_data(self):
        form_data = {"name": "Napoleon"}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_dish_search_form_empty_data(self):
        form = DishSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_cook_search_form_valid_data(self):
        form_data = {"cook": "Mark"}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["cook"], form_data["cook"])

    def test_cook_search_form_empty_data(self):
        form = CookSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["cook"], "")

    def test_cook_creation_form_fields(self):
        form = CookCreationForm()
        expected_fields = [
            "username", "first_name", "last_name", "years_of_experience",
            "password1", "password2"
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

