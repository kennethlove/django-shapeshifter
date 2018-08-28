# django-shapeshifter

A common problem in Django is how to have a view, especially a class-based view
that can display and process multiple forms at once. `django-shapeshifter` aims
to make this problem much more trivial.

Right now, `django-shapeshifter` can handle any (well, theoretically) number of
forms in a single view. A view class is provided for multiple standard forms
or model forms. To mix and match these form types, you'll need to do a little
extra work. Here's how to use the package:

## Installation

`$ pip install django-shapeshifter`

You should not need to add `shapeshifter` to your `INSTALLED_APPS`.

## Usage

You use `django-shapeshifter` just like you use Django's built-in class-based
views. You should be able to use the provided views with any mixins you're
already using in your project, too, like `LoginRequiredMixin`.

Let's look at using the view with a few standard forms:

*interests/views.py*
```python
from django.urls import reverse_lazy

from shapeshifter.views import MultiFormView

from . import forms


class InterestFormsView(MultiFormView):
    form_classes = (forms.ContactForm, forms.InterestsForm, forms.GDPRForm)
    template_name = 'interests/forms.html'
    success_url = reverse_lazy('interests:thanks')
```

But what do you need to do in the template? The view's context will contain
a new member, `forms`, that you can iterate over to display each form:

*interests/templates/interests/forms.html*
```html
{% extends 'layout.html' %}

{% block content %}
<h3>Please fill out your interests below!</h3>

<form method="POST">
{% csrf_token %}
{% for form in forms %}
    {{ form.as_p }}
{% endfor %}
    <input type="submit" value="Save" />
</form>
{% endblock content %}
```

This will generate a template with all three forms, in succession, inside of a
single `<form>` tag. **All of the forms must be submitted together.** After
submission, Django will fill each form in with the appropriate submitted data,
validate them, and then redirect to your `success_url`.

But with just the above code, nothing will happen with the form data. To control
that, you need to override the `forms_valid` method in your view. Here's what
that might look like:

*interests/views.py*
```python
class InterestsFormView(MultiFormView):
   ...
   def forms_valid(self):
       forms = self.get_forms()
       contact_form = forms['contactform']
       interest_form = forms['interestsform']
       gdpr = forms['gdprform']
       
       if not gdpr.data['accept']:
           messages.error("You must accept the GDPR terms.")
           return HttpResponseRedirect(reverse_lazy('interests:forms'))
       salesforce_client.send(zip(contact_form.data.items(),
                                  interest_form.data.items()))
       return super().forms_valid()
```

The above code isn't meant to be a complete example but should give you an idea
of what would be done to handle the form data.

### What about model forms?

All of the above code is valid for model forms, too, with one exception. For
model forms, instead of extending `MultiFormView`, you'll extend
`MultiModelFormView`. There are two major differences between the classes but
the most important one is that `forms_valid` will call `form.save()` on each
form. Here is an example allowing a user to edit their `User` `first_name` and `last_name`, and their first `Profile` `name` on one form:

*my_app/models.py*
```python
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, realted_name='profiles', on_delete=models.CASCADE)
```

*my_app/forms.py*
```python
from django.contrib.auth.models import User

from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
        ]

        labels = {
            'name': 'Profile Name',
        }
```

*my_app/views.py*
```python
from shapeshifter.views import MultiModelFormView

from .forms import UserForm, ProfileForm

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, MultiModelFormView):
    form_classes = (UserForm, ProfileForm)
    template_name = 'my_app/forms.html'
    success_url = reverse_lazy('home')
    success_message = 'Your name and profile name have been updated.'

    def get_instances(self):
        instances = {
            'userform': self.request.user,
            'groupform': Profile.objects.filter(
                user=self.request.user,
            ).first(),
        }

        return instances
```

### What if I want to mix model and standard form?

That's fine! You will have to override `forms_valid` in your view to handle the
processing of each form but everything else should work exactly the same.

## API

`MultiFormView` (and `MultiModelFormView` by inheritance) extends Django's
`TemplateView`. Additionally it adds a few methods for the instantiation and
processing of the forms. Any and all of these can be overwritten to customize
the behavior of your views.

Below is each attribute and their default value, and each method with its
signature and return value.

### Attributes

* `initial = {}` - Initial values for each form. Should be a `dict` formatted
with the following format:

```python
initial = {
    'contactform': {
        'name': 'Katherine Johnson'
    }
}
```

where `ContactForm` is the class name of the form you're providing initial
values for.

* `form_classes = None` - a list or tuple of `Form` (or `ModelForm` if using
`MultiModelFormView`) classes. **Do not instantiate the class, just provide the
name**).

* `success_url = None` - the URL to redirect users to once the forms are all filled in
correctly. This can be a URL or a `reverse_lazy` instance.

### Methods

* `get_form_classes(self)` - Returns the view's `form_classes` attribute.
Override this method if you need to dynamically set the forms that should be
included in the view.

* `get_forms(self) -> dict` - Instantiates each form, using the `kwargs` from
`get_form_kwargs` and returns them all as a dict with the key being a standardized
version of the form's class name. Override this if you need to change how the
forms are instantiated.

* `get_form_class_name(self, form_class) -> str` - Converts the form's class
name into a lowercase string. `ContactForm` will become `contactform`. You can
override this to provide for a different standardized name for your forms.

* `get_form_kwargs(self, form_class) -> dict` - Returns a dict of keyword
arguments for the form's creation. Prefixes each form with the lowercased class
name, provides any `initial` arguments for the form, and, if the view was
requested as either `POST` or `PUT`, provides both `data` and `files` to the
form. For `MultiModelFormView`, this method also provides the `instance` for the
form. Override this method to add or change the form kwargs.

* `validate_forms(self) -> bool` - Calls `form.is_valid()` for each form and
returns the result for the entire set of forms. Override this method if your
forms require any special validation steps.

* `forms_valid(self)` - This method is called if all forms pass validation. In
`MultiFormView`, this method simply redirects to the `success_url`. For the 
model-based version, `MultiModelFormView`, this method calls `form.save()` on
each form and then redirects. Override this method to change what happens
when the forms are all valid.

* `forms_invalid(self)` - If any of the forms fail their validation check, this
method is executed. By default, it re-renders the view, presenting the forms
with their errors. You can override this method if you need something else to
happen when not all forms are valid.

### `MultiModelFormView`'s extra attributes and methods

As mentioned above, a few things are handled differently in `MultiModelFormView`.

* `instances = {}` - This attribute should be a dict with lowercase form class
names as keys. The values should be the instance to use for the form.

* `get_instances(self)` - Returns the value of `instances`. Override this if
you need to dynamically fetch the instances for the forms.

## Contributing

Thank you for your interest, time, and energy! Contributions are always
welcome and will be reviewed as quickly as possible (that said, we're all
volunteers with other jobs/responsibilities so it might be awhile).

Please fork this repository and make your changes in the `shapeshifter` package.
Be sure to add a test for any functionality changes. Once all tests pass, you
can submit a pull request with your changes, the rationale behind them, and
any special steps the maintainers will need to take to test your changes or
replicate the bug you're fixing. **Be sure to include adding your name to the
following list of contributors!**

### Contributors

* Kenneth Love
* Lacey Williams Henschel
* Tim Allen

## What's with the name? And the version?

The original name was already taken so a new one had to be found. Since this
package deals with multiple forms, `shapeshifter` was a good pun (shapeshifters
can take on many forms).

The version number is based on the date of release.
