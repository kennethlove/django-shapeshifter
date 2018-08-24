from django import forms

from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ("title", "slug", "published", "content")


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
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
