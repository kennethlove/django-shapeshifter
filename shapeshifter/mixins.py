from django.contrib import messages


class MultiSuccessMessageMixin(object):
    """
    Add a success message on successful multiple forms submission.
    """
    success_message = None

    def get_success_message(self):
        return self.success_message

    def forms_valid(self):
        response = super(MultiSuccessMessageMixin, self).forms_valid()

        success_message = self.get_success_message()
        if success_message:
            messages.success(self.request, success_message)

        return response
