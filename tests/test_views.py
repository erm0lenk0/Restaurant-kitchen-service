from django.test import TestCase
from django.urls import reverse
from kitchen_core.models import DishType, Dish, Cook
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class DishTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="chef",
            password="qaz2wsx3edc",
        )
        self.client.login(username="chef", password="qaz2wsx3edc")

    def test_create_dish_type(self):
        response = self.client.post(reverse("kitchen_core:dish-type-create"), {"name": "Pizza"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DishType.objects.filter(name="Pizza").exists())

    def test_update_dish_type(self):
        dish_type = DishType.objects.create(name="Pizza")
        response = self.client.post(
            reverse(
                "kitchen_core:dish-type-update",
                    args=[dish_type.pk]),
            {"name": "Pizza"},
        )
        self.assertEqual(response.status_code, 302)
        dish_type.refresh_from_db()
        self.assertEqual(dish_type.name, "Pizza")

    def test_delete_dish_type(self):
        dish_type = DishType.objects.create(name="Pizza")
        url = reverse("kitchen_core:dish-type-delete", args=[dish_type.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DishType.objects.filter(pk=dish_type.pk).exists())

    def test_list_dish_types(self):
        DishType.objects.create(name="Pizza")
        DishType.objects.create(name="Pasta")
        response = self.client.get(reverse("kitchen_core:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertContains(response, "Pasta")

    def test_dish_type_detail_view(self):
        dish_type = DishType.objects.create(name="Desserts")
        url = reverse("kitchen_core:dish-type-detail", args=[dish_type.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Desserts")

    def test_search_dish_type(self):
        DishType.objects.create(name="Desserts")
        DishType.objects.create(name="Pasta")
        response = self.client.get(reverse("kitchen_core:dish-type-list") + "?q=desserts")
        self.assertContains(response, "Desserts")
        self.assertContains(response, "Pasta")

    def test_pagination_dish_type(self):
        for i in range(15):
            DishType.objects.create(name=f"Type {i}")
        response_page_1 = self.client.get(reverse("kitchen_core:dish-type-list") + "?page=1")
        self.assertEqual(response_page_1.status_code, 200)
        self.assertEqual(len(response_page_1.context["dish_type_list"]), 5)

        response_page_2 = self.client.get(reverse("kitchen_core:dish-type-list") + "?page=2")
        self.assertEqual(response_page_2.status_code, 200)
        self.assertEqual(len(response_page_2.context["dish_type_list"]), 5)

class DishTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="chef",
            password="qaz2wsx3edc",
            first_name="Vanessa",
            last_name="Maev",
        )
        self.client.login(username="chef", password="qaz2wsx3edc")

        self.dish_type = DishType.objects.create(name="Main Course")

        self.default_dish_data = {
            "name": "Varenyky",
            "description": "Traditional Ukrainian dumplings",
            "price": "12.50",
            "dish_type": self.dish_type.id,
            "cooks": [self.user.id],
        }

    def create_dish(self):
        dish = Dish.objects.create(
            name="Varenyky",
            description="Traditional Ukrainian dumplings",
            price="12.50",
            dish_type=self.dish_type,
        )
        dish.cooks.add(self.user)
        return dish

    def test_create_dish(self):
        response = self.client.post(
            reverse("kitchen_core:dish-create"),
            self.default_dish_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name="Varenyky").exists())


    def test_update_dish(self):
        dish = self.create_dish()
        updated_data = self.default_dish_data.copy()
        updated_data["name"] = "Updated Varenyky"

        response = self.client.post(
            reverse("kitchen_core:dish-update", args=[dish.pk]),
            updated_data,
        )
        self.assertEqual(response.status_code, 302)
        dish.refresh_from_db()
        self.assertEqual(dish.name, "Updated Varenyky")

    def test_delete_dish(self):
        dish = self.create_dish()
        response = self.client.post(
            reverse("kitchen_core:dish-delete", args=[dish.pk]),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(pk=dish.pk).exists())

    def test_dish_list_display(self):
        self.create_dish()
        response = self.client.get(reverse("kitchen_core:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Varenyky")

    def test_dish_cook_display(self):
        dish = self.create_dish()
        response = self.client.get(reverse("kitchen_core:dish-detail", args=[dish.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_dish_search(self):
        self.create_dish()
        response = self.client.get(reverse("kitchen_core:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Varenyky")

    def test_dish_pagination_dish(self):
        for i in range(7):
            Dish.objects.create(
                name=f"Dish {i}",
                description=f"Test Dish {i}",
                price="12.50",
                dish_type=self.dish_type,
            )
        response = self.client.get(reverse("kitchen_core:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dish 0")
        self.assertNotContains(response, "Dish 6")

    def test_dish_detail_view(self):
        dish = self.create_dish()
        response = self.client.get(reverse("kitchen_core:dish-detail", args=[dish.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Traditional Ukrainian dumplings")
        self.assertContains(response, "Main Course")

    def test_toggle_assign_to_dish(self):
        dish = self.create_dish()
        dish.cooks.remove(self.user)

        # Назначение повара
        response = self.client.get(
            reverse("kitchen_core:toggle-assign-dish", args=[dish.pk])
        )
        self.assertEqual(response.status_code, 302)
        dish.refresh_from_db()  # обновляем объект из базы
        self.assertIn(self.user, dish.cooks.all())

        # Повторное нажатие — отказ от приготовления
        response = self.client.get(
            reverse("kitchen_core:toggle-assign-dish", args=[dish.pk])
        )
        self.assertEqual(response.status_code, 302)
        dish.refresh_from_db()  # снова обновляем
        self.assertNotIn(self.user, dish.cooks.all())

class CookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="chef",
            password="qaz2wsx3edc",
            first_name="Vanessa",
            last_name="Maev",
            years_of_experience=5,
        )
        self.client.login(username="chef", password="qaz2wsx3edc")

    def create_cook(
            self,
            username="cook1",
            first_name="Anna",
            last_name="Teikoku",
            experience=3,
            password="qaz2wsx3edc4rfv"
    ):
        return get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            years_of_experience=experience,
        )

    def test_cook_list_display(self):
        self.create_cook()
        response = self.client.get(reverse("kitchen_core:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anna Teikoku")

    def test_cook_search(self):
        self.create_cook(username="cook1", first_name="John", last_name="Doe")
        self.create_cook(username="cook2", first_name="Jone", last_name="Smith")

        response = self.client.get(
            reverse("kitchen_core:cook-list"),
            {"cook": "Jone"})
        self.assertContains(response, "Jone Smith")
        self.assertNotContains(response, "John Doe")

    def test_cook_pagination(self):
        for i in range(7):
            self.create_cook(username=f"cook{i}", first_name=f"Name{i}", last_name="Test")

        response = self.client.get(reverse("kitchen_core:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cook_list"]), 5)

        response_page_2 = self.client.get(reverse("kitchen_core:cook-list") + "?page=2")
        self.assertEqual(len(response_page_2.context["cook_list"]), 3)

    def test_cook_detail_display(self):
        cook = self.create_cook(first_name="Anna", last_name="Teikoku")
        dish = Dish.objects.create(
            name="Varenyky",
            description="Traditional Ukrainian dumplings",
            price="12.50",
            dish_type=DishType.objects.create(name="Desserts"),
        )
        dish.cooks.add(cook)

        response = self.client.get(reverse("kitchen_core:dish-detail", args=[dish.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Traditional Ukrainian dumplings")
        self.assertContains(response, "Desserts")

    def test_cook_update(self):
        cook = self.create_cook(username="cook", password="qaz2wsx3edc")
        self.client.login(username="cook", password="qaz2wsx3edc")

        response = self.client.post(
            reverse("kitchen_core:cook-update", args=[cook.pk]),
            {
                "username": "cook1",
                "first_name": "John",
                "last_name": "Doe",
                "years_of_experience": 5,
                "email": "john@example.com",
            },
        )

        if response.status_code != 302:
            print(response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        cook.refresh_from_db()
        self.assertEqual(cook.first_name, "John")
        self.assertEqual(cook.years_of_experience, 5)

    def test_cook_delete(self):
        cook = self.create_cook()
        self.client.login(username="cook", password="qaz2wsx3edc")

        response = self.client.post(reverse("kitchen_core:cook-delete", args=[cook.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(pk=cook.pk).exists())