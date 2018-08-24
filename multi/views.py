from django.urls import reverse_lazy

from . import forms, mixins


class Create(mixins.MultiModelFormView):
    form_classes = (forms.PostForm, forms.AuthorForm)
    template_name = 'multi/forms.html'
    success_url = reverse_lazy('create')


class Other(mixins.MultiFormView):
    form_classes = (forms.NumbersForm, forms.EmailForm)
    template_name = 'multi/forms.html'
    success_url = reverse_lazy('others')