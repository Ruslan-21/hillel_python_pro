from django import forms


class CartAddBookForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )