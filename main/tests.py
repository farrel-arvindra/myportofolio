from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Interest


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.interest = Interest.objects.create(
            title="Machine Learning",
            description="Mempelajari model predictive analytics dan pengembangan AI.",
            since=2024,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_interest_url_is_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_interest"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "interest.html")

    def test_interest_data_appears_on_page_when_data_exists(self):
        response = self.client.get(reverse("main:show_interest"))

        self.assertContains(response, "Memuat data interest")
        self.assertNotContains(response, self.interest.title)
        self.assertNotContains(response, self.interest.description)

    def test_empty_interest_page_starts_with_loading_state(self):
        Interest.objects.all().delete()
        response = self.client.get(reverse("main:show_interest"))

        self.assertContains(response, "Belum ada interest yang ditambahkan atau ditemukan.")
        self.assertContains(response, "hide")
        data_response = self.client.get(reverse("main:get_interests_json"))
        self.assertEqual(data_response.json(), [])

    def test_interest_add_modal_is_only_rendered_for_superuser(self):
        guest_response = self.client.get(reverse("main:show_interest"))
        self.assertNotContains(guest_response, 'id="add-interest-modal"')

        User.objects.create_user(username="visitor", password="password")
        self.client.login(username="visitor", password="password")
        user_response = self.client.get(reverse("main:show_interest"))
        self.assertNotContains(user_response, 'id="add-interest-modal"')

        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(admin)
        admin_response = self.client.get(reverse("main:show_interest"))
        self.assertContains(admin_response, 'id="add-interest-modal"')

    def test_interests_json_is_available_to_anonymous_users_with_star_data(self):
        user = User.objects.create_user(username="visitor", password="password")
        self.interest.interested_users.add(user)

        response = self.client.get(reverse("main:get_interests_json"))

        self.assertEqual(response.status_code, 200)
        interest_data = response.json()[0]
        self.assertEqual(interest_data["fields"]["star_count"], 1)
        self.assertFalse(interest_data["fields"]["is_starred"])

    def test_interests_json_reports_current_users_star(self):
        user = User.objects.create_user(username="visitor", password="password")
        self.interest.interested_users.add(user)
        self.client.force_login(user)

        response = self.client.get(reverse("main:get_interests_json"))

        self.assertTrue(response.json()[0]["fields"]["is_starred"])

    def test_interests_json_filters_by_title(self):
        Interest.objects.create(title="Baking", description="Making bread")

        response = self.client.get(
            reverse("main:get_interests_json"),
            {"title": "machine"},
        )

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["fields"]["title"], "Machine Learning")

    def test_interest_ajax_creation_requires_superuser(self):
        url = reverse("main:create_interest_ajax")

        anonymous_response = self.client.post(
            url,
            {"title": "Reading", "description": "Books", "since": 2020},
        )
        self.assertEqual(anonymous_response.status_code, 403)

        User.objects.create_user(username="visitor", password="password")
        self.client.login(username="visitor", password="password")
        user_response = self.client.post(
            url,
            {"title": "Reading", "description": "Books", "since": 2020},
        )
        self.assertEqual(user_response.status_code, 403)
        self.assertFalse(Interest.objects.filter(title="Reading").exists())

    def test_interest_ajax_creation_returns_created_interest(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(admin)

        response = self.client.post(
            reverse("main:create_interest_ajax"),
            {
                "title": "  <b>Reading</b>  ",
                "description": "<p>Books and stories</p>",
                "since": 2020,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["title"], "Reading")
        self.assertEqual(response.json()["fields"]["description"], "Books and stories")

    def test_interest_ajax_creation_returns_validation_errors(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(admin)

        response = self.client.post(
            reverse("main:create_interest_ajax"),
            {"title": "<b></b>", "description": "<p></p>", "since": 2020},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertIn("description", response.json()["errors"])