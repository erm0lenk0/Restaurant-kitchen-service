from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen_core.models import Dish, DishType


class CookDishRelationsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="chef",
            password="qaz2wsx3edc",
            first_name="Gordon",
            last_name="Ramsay",
        )
        self.client.login(username="chef", password="qaz2wsx3edc")
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Beef Wellington",
            description="Classic British dish",
            price=250,
            dish_type=self.dish_type,
        )

    def test_assign_dish_to_cook(self):
        self.dish.cooks.add(self.user)
        self.assertIn(self.user, self.dish.cooks.all())

    def test_unassing_dish_from_cook(self):
        self.dish.cooks.add(self.user)
        self.dish.cooks.remove(self.user)
        self.assertNotIn(self.user, self.dish.cooks.all())

    def test_dish_appears_in_cook_detail_view(self):
        self.dish.cooks.add(self.user)
        url = reverse("kitchen_core:cook-detail", args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beef Wellington")
        self.assertContains(response, "Main Course")
