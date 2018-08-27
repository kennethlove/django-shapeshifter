from django.urls import reverse_lazy

from multiform import views as mf_views
from testapp import forms


class Membership(mf_views.MultiModelFormView):
    form_classes = (forms.UserForm, forms.GroupForm)
    template_name = 'testapp/forms.html'
    success_url = reverse_lazy('membership')


class Other(mf_views.MultiFormView):
    form_classes = (forms.NumbersForm, forms.EmailForm)
    template_name = 'testapp/forms.html'
    success_url = reverse_lazy('other')