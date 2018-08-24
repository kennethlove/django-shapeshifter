from unittest import mock

from django.test import TestCase, RequestFactory

from multi.views import Other

initial_data = {"numbersform": {"minimum": 42}}


class MultiFormViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_multiple_forms_rendered(self):
        """Multiple forms should be rendered to the template"""
        request = self.factory.get("/")
        response = Other.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Minimum")
        self.assertContains(response, "Email")

    def test_prefixes(self):
        """Each form should have an auto-generated prefix"""
        request = self.factory.get("/")
        response = Other.as_view()(request)
        self.assertIn("numbersform", response.context_data)
        self.assertIn("emailform", response.context_data)

    @mock._patch_object(Other, "initial", initial_data)
    def test_initial(self):
        """A form should be able to have initial data"""
        request = self.factory.get("/")
        response = Other.as_view()(request)
        self.assertContains(response, "42")

    def test_form_validation(self):
        """Forms should still provide errors"""
        request = self.factory.post(
            "/", data={
                "numbersform-minimum": 42,
                "numbersform-maximum": 1,
                "emailform-email_address": "test@example.com",
                "emailform-message": "Hey"
            }
        )
        response = Other.as_view()(request)
        self.assertTrue(response.context_data['numbersform'].errors)
        self.assertFalse(response.context_data['emailform'].errors)
