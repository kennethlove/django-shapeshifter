from unittest import mock

from django.contrib.auth.models import User, Group

from testapp.views import Membership

initial_data = {"groupform": {"name": "Admins"}}


def test_multiple_forms_rendered(request_factory):
    """Multiple forms should be rendered to the template"""
    request = request_factory().get("/")
    response = Membership.as_view()(request)
    assert response.status_code == 200
    assert "Username" in response.rendered_content
    assert "Name" in response.rendered_content


def test_multiple_forms_success_mixin(request_factory):
    """Multiple forms should be rendered to the template"""
    request = request_factory().get("/")
    response = Membership.as_view()(request)
    assert response.status_code == 200
    assert "this is a success message" in response.rendered_content


def test_prefixes(request_factory):
    """Each form should have an auto-generated prefix"""
    request = request_factory().get("/")
    response = Membership.as_view()(request)
    assert "userform" in response.context_data
    assert "groupform" in response.context_data


@mock.patch.object(Membership, "initial", initial_data)
def test_initial(request_factory):
    """A form should be able to have initial data"""
    request = request_factory().get("/")
    response = Membership.as_view()(request)
    assert "Admins" in response.rendered_content


@mock.patch.object(Membership, "forms_valid", lambda: None)
def test_form_validation(request_factory):
    """Forms should still provide errors"""
    request = request_factory().post(
        "/",
        data={
            "userform-first_name": "Katherine",
            "userform-last_name": "Johnson",
            "groupform-name": "Admins",
        },
    )
    response = Membership.as_view()(request)
    context = response.context_data
    assert context["userform"].errors
    assert not context["groupform"].errors


def test_getting_instances(request_factory):
    group = Group.objects.create(name="Admins")
    instances = {"groupform": group}

    request = request_factory().get("/")
    with mock.patch("testapp.views.Membership.get_instances", return_value=instances):
        response = Membership.as_view()(request)
    assert group.name in response.rendered_content

    group.delete()


def test_form_validation(request_factory):
    """Forms should still provide errors"""
    request = request_factory().post(
        "/",
        data={
            "userform-first_name": "Katherine",
            "userform-last_name": "Johnson",
            "userform-username": "KJohnson",
            "groupform-name": "Admins",
        },
    )
    with mock.patch.object(Group, "save") as mock_group, mock.patch.object(
        User, "save"
    ) as mock_user:
        Membership.as_view()(request)
        mock_user.assert_called_once()
        mock_group.assert_called_once()
