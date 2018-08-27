from unittest import mock

import pytest
from django.core.exceptions import ImproperlyConfigured
from testapp.views import Other

initial_data = {"numbersform": {"minimum": 42}}


def test_multiple_forms_rendered(request_factory):
    """Multiple forms should be rendered to the template"""
    request = request_factory().get("/")
    response = Other.as_view()(request)
    assert response.status_code == 200
    assert "Minimum" in response.rendered_content
    assert "Email" in response.rendered_content


def test_prefixes(request_factory):
    """Each form should have an auto-generated prefix"""
    request = request_factory().get("/")
    response = Other.as_view()(request)
    context = response.context_data
    assert "numbersform" in context
    assert "emailform" in context


@mock.patch.object(Other, "initial", initial_data)
def test_initial(request_factory):
    """A form should be able to have initial data"""
    request = request_factory().get("/")
    response = Other.as_view()(request)
    assert "42" in response.rendered_content


def test_form_validation(request_factory):
    """Forms should still provide errors"""
    request = request_factory().post(
        "/",
        data={
            "numbersform-minimum": 42,
            "numbersform-maximum": 1,
            "emailform-email_address": "test@example.com",
            "emailform-message": "Hey",
        },
    )
    response = Other.as_view()(request)
    context = response.context_data
    assert context["numbersform"].errors
    assert not context["emailform"].errors


def test_success_url():
    assert Other.success_url == "/other/"


@mock.patch.object(Other, "success_url", None)
def test_no_success_url():
    with pytest.raises(ImproperlyConfigured):
        Other().get_success_url()


def test_forms_valid(request_factory):
    request = request_factory().post(
        "/",
        data={
            "numbersform-minimum": 2,
            "numbersform-maximum": 4,
            "emailform-email_address": "test@example.com",
            "emailform-message": "Hey",
        },
    )
    response = Other.as_view()(request)
    assert response.status_code == 302


@mock.patch.object(Other, "post")
def test_put(mock_method, request_factory):
    request = request_factory().put(
        "/",
        data={
            "numbersform-minimum": 2,
            "numbersform-maximum": 4,
            "emailform-email_address": "test@example.com",
            "emailform-message": "Hey",
        },
    )
    Other.as_view()(request)
    mock_method.assert_called()
