from django.urls import reverse_lazy

from shapeshifter import views as shape_views
from shapeshifter.mixins import MultiSuccessMessageMixin
from testapp import forms


class Membership(MultiSuccessMessageMixin, shape_views.MultiModelFormView):
    form_classes = (forms.UserForm, forms.GroupForm)
    template_name = 'testapp/forms.html'
    success_url = reverse_lazy('membership')
    success_message = 'this is a success message'


class Other(shape_views.MultiFormView):
    form_classes = (forms.NumbersForm, forms.EmailForm)
    template_name = 'testapp/forms.html'
    success_url = reverse_lazy('other')
