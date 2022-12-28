from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)


deliever_or_pickup_choices = (
        (True, 'Доставка'),
        (False, 'Самовывоз'),)
cash_or_card_choices = (
        (True, 'Наличные'),
        (False, 'Карта'),)


class OrderFillForm(forms.Form):
    deliever_or_pickup = forms.ChoiceField(
        widget=forms.RadioSelect,choices=deliever_or_pickup_choices)
    cash_or_card = forms.ChoiceField(
        widget=forms.RadioSelect,choices=cash_or_card_choices)