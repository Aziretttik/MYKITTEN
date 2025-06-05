from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2']



class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label='Код подтверждения',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите код подтверждения',
            'maxlength': '6',
            'minlength': '6'
        }),
        min_length=6,
        max_length=6,
        required=True,
        error_messages={
            'required': 'Пожалуйста, введите код подтверждения',
            'min_length': 'Код должен содержать 6 цифр',
            'max_length': 'Код должен содержать 6 цифр'
        }
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit():
            raise forms.ValidationError('Код должен содержать только цифры')
        return code
