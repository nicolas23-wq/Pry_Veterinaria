from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 21)],  
        coerce=int,
        label="Cantidad",
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('quantity', None)
        super().__init__(*args, **kwargs)
        if product:
            max_quantity = min(20, product.stock)  
            self.fields[''].choices = [(i, str(i)) for i in range(1, max_quantity + 1)]