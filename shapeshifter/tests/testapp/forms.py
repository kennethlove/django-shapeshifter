from django import forms
from django.contrib.auth.models import Group, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)


class NumbersForm(forms.Form):
    minimum = forms.IntegerField()
    maximum = forms.IntegerField()

    def clean(self) -> dict:
        cleaned_data = super().clean()
        if cleaned_data["minimum"] >= cleaned_data["maximum"]:
            raise forms.ValidationError(
                "minimum cannot be greater than or equal to maximum"
            )
        return cleaned_data


class EmailForm(forms.Form):
    email_address = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())
