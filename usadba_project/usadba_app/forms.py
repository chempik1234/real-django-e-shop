from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OpinionForm(forms.Form):
    order_unique_id = forms.CharField(label="Номер заказа для подтверждения отзыва", min_length=1,
                                      max_length=30, required=False)
    text = forms.CharField(label="Текст отзыва", min_length=1, max_length=400)
    file = forms.ImageField(label="Прикрепить фото", required=False)
    # field_order = ["age", "name", "email", "ads"]


class DBLoginForm(UserCreationForm):
    #username = forms.CharField(label="Никнейм", required=True, max_length=150)
    surname = forms.CharField(label="Фамилия", required=True, max_length=150)
    name = forms.CharField(label="Имя", required=True, max_length=150)
    email = forms.EmailField(label="Логин / Почта", required=True, max_length=254)
    #password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput, max_length=128)
    #repeat_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, required=True,
    #                                  max_length=128)
    #remember_me = forms.BooleanField(label='Запомнить меня', required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже есть")
        return email

    # def clean_repeat_password(self):
    #     password = self.cleaned_data['password']
    #     repeat_password = self.cleaned_data['repeat_password']
    #     if repeat_password != password:
    #         raise forms.ValidationError("Пароли не совпадают")
    #     return repeat_password

    class Meta:
        model = User
        fields = ("username", "surname", "name", "email",)

    def save(self, commit=True):
        user = super(DBLoginForm, self).save(commit=False)
        user.first_name = self.cleaned_data["name"]
        user.last_name = self.cleaned_data["surname"]
        user.email = self.cleaned_data["email"]
        user.password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user


class SignInForm(forms.Form):
    email = forms.EmailField(label='Почта', required=True, max_length=254)
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput, max_length=128)
    # remember_me = forms.BooleanField(label='Запомнить меня', required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователя с такой почтой нет")
        return email

    def clean_password(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not User.objects.filter(email=email,password=password).exists():
            raise forms.ValidationError("Неправильный пароль")
        return password