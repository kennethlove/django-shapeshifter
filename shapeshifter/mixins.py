from django.contrib import messages


class SuccessMessageMixin(object):
    """
    Add a success message on successful form submission.
    """
    success_message = None

    def forms_valid(self):
        response = super(SuccessMessageMixin, self).forms_valid()
        if self.success_message:
            messages.success(self.request, self.success_message)

        return response
