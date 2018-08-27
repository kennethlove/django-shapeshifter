from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.Membership.as_view(), name="membership"),
    path("other/", views.Other.as_view(), name="other"),
]
