from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class MultiFormView(TemplateView):
    initial = {}
    form_classes = None
    success_url = None

    def get_context_data(self, **kwargs):
        if "forms" not in kwargs:
            forms = self.get_forms()
            kwargs["forms"] = forms.values()
            kwargs.update(**forms)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)

    def get_initial(self):
        return self.initial.copy()

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self) -> dict:
        form_classes = self.get_form_classes()
        return {
            self.get_form_class_name(form_class): form_class(
                **self.get_form_kwargs(form_class)
            )
            for form_class in form_classes
        }

    def get_form_class_name(self, form_class) -> str:
        return form_class.__name__.lower()

    def get_form_kwargs(self, form_class) -> dict:
        class_name = self.get_form_class_name(form_class)

        kwargs = {"prefix": class_name}

        initial = self.get_initial()
        if class_name in initial:
            kwargs["initial"] = initial[class_name]

        if self.request.method in ("POST", "PUT"):
            kwargs.update({"data": self.request.POST, "files": self.request.FILES})
        return kwargs

    def forms_valid(self):
        """All forms are valid, redirect to the success_url"""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self):
        """At least one form is invalid, render all forms"""
        return self.render_to_response(self.get_context_data())

    def validate_forms(self):
        """Make sure all forms are valid"""
        forms = self.get_forms()
        return all(form.is_valid() for form in forms.values())

    def post(self, request, *args, **kwargs):
        if self.validate_forms():
            return self.forms_valid()
        return self.forms_invalid()

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class MultiModelFormView(MultiFormView):
    instances = {}

    def get_instances(self):
        return self.instances

    def get_form_kwargs(self, form_class):
        kwargs = super().get_form_kwargs(form_class)
        class_name = self.get_form_class_name(form_class)
        instances = self.get_instances()
        if class_name in instances:
            kwargs.update({'instance': instances[class_name]})
        return kwargs

    def forms_valid(self):
        for form in self.get_forms().values():
            form.save()
        return super().forms_valid()
