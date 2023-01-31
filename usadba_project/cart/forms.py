from django import forms
from usadba_app.models import check_float


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)


deliver_or_pickup_choices = (
        (True, 'Доставка'),
        (False, 'Самовывоз'),)
cash_or_card_choices = (
        (True, 'Наличные'),
        (False, 'Карта'),)


class OrderFillForm(forms.Form):
    deliver_or_pickup = forms.ChoiceField(
        widget=forms.RadioSelect,choices=deliver_or_pickup_choices)
    cash_or_card = forms.ChoiceField(
        widget=forms.RadioSelect,choices=cash_or_card_choices)
    location = forms.CharField(required=False)

    def clean_location(self):
        location = self.cleaned_data['location']
        print("location", location)
        if self.cleaned_data['deliver_or_pickup'] == True and not location:
            raise forms.ValidationError("Ошибка формы: если выбрана доставка, должно быть выбрано место.")
        if location:
            if location.find(',') <= 0 or location.find(',') >= len(location) - 1:
                raise forms.ValidationError("Ошибка формы: неправильный формат местоположения (нужно, чтобы между "
                                            "широтой и долготой была запятая), введённые данные: " + str(location))
            if not check_float(location[: location.index(',')]) or not check_float(location[location.index(',') + 1:]):
                raise forms.ValidationError("Ошибка формы: неправильный формат местоположения, введённые данные: " +
                                            str(location))
        return location
