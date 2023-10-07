from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput, help_text='Senha de no mínimo 8 caracteres contendo ao menos uma letra e um número!')
    password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label='Staff', required=False)


    class Meta:
        model = CustomUser
        fields = ('username', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Senha com 8 caracteres ou mais contendo pelo menos uma letra e um número."

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'is_staff')