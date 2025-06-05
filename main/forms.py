from django import forms
from .models import Cat, AdoptionRequest


class CatCreateForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'color', 'description', 'photo', 'health_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя кошки'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Возраст'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Порода'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Окрас'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'health_status': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Состояние здоровья'}),
        }

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Расскажите, почему вы хотите взять именно этого котика'}),
        }


class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'color', 'description', 'photo', 'health_status', 'is_adopted']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите имя котика'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Укажите возраст'
            }),
            'breed': forms.TextInput(attrs={
                'placeholder': 'Укажите породу'
            }),
            'color': forms.TextInput(attrs={
                'placeholder': 'Укажите окрас'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Опишите характер и привычки котика'
            }),
            'health_status': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Опишите состояние здоровья котика'
            }),
            'is_adopted': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите код подтверждения',
        })
    )
