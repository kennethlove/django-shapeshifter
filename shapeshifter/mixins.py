from django.contrib import messages


class MultiSuccessMessageMixin(object):
    """
    Add a success message on successful multiple forms submission.
    """
    success_message = None

    def forms_valid(self):
        response = super(MultiSuccessMessageMixin, self).forms_valid()
        if self.success_message:
            messages.success(self.request, self.success_message)

        return response
