from django import forms
from django.utils.translation import gettext_lazy as _


class CartAddBookForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label=_("Quantity"),
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
        label=_("Override"),
    )