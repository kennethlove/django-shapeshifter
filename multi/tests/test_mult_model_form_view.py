from unittest import mock

from django.test import TestCase, RequestFactory

from multi.models import Author
from multi.views import Create

author, _ = Author.objects.get_or_create(name='Katherine Johnson')
instances = {'authorform': author}
initial_data = {"authorform": {"name": "Alice"}}


class MultiModelFormViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_multiple_forms_rendered(self):
        """Multiple forms should be rendered to the template"""
        request = self.factory.get("/")
        response = Create.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Title")
        self.assertContains(response, "Name")

    def test_prefixes(self):
        """Each form should have an auto-generated prefix"""
        request = self.factory.get("/")
        response = Create.as_view()(request)
        self.assertIn("postform", response.context_data)
        self.assertIn("authorform", response.context_data)

    @mock._patch_object(Create, "initial", initial_data)
    def test_initial(self):
        """A form should be able to have initial data"""
        request = self.factory.get("/")
        response = Create.as_view()(request)
        self.assertContains(response, "Alice")

    @mock._patch_object(Create, "forms_valid", lambda: None)
    def test_form_validation(self):
        """Forms should still provide errors"""
        request = self.factory.post(
            "/",
            data={
                "postform-title": "Katherine Johnson: A Lifetime of STEM",
                "postform-published": True,
                "postform-content": "Katherine Johnson loved to count",
                "authorform-name": "Katherine Johnson",
            },
        )
        response = Create.as_view()(request)
        self.assertTrue(response.context_data["postform"].errors)
        self.assertFalse(response.context_data["authorform"].errors)

    @mock._patch_object(Create, 'instances', instances)
    def test_getting_instances(self):
        request = self.factory.get('/')
        response = Create.as_view()(request)
        self.assertContains(response, author.name)
