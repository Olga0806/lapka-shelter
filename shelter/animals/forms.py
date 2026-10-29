from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Animal, AnimalPhoto, Application


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'breed', 'age', 'gender', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AnimalPhotoForm(forms.ModelForm):
    class Meta:
        model = AnimalPhoto
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class ApplicationForm(forms.ModelForm):
    """Анкета клиента — без статуса."""
    class Meta:
        model = Application
        fields = ['full_name', 'phone', 'age', 'housing',
                  'family_size', 'other_animals', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+7 999 000-00-00'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 18}),
            'housing': forms.Select(attrs={'class': 'form-select'}),
            'family_size': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'other_animals': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кошка, собака — или оставьте пустым'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class KinologApplicationForm(forms.ModelForm):
    """Для кинолога — со статусом."""
    class Meta:
        model = Application
        fields = ['full_name', 'phone', 'age', 'housing',
                  'family_size', 'other_animals', 'comment', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'housing': forms.Select(attrs={'class': 'form-select'}),
            'family_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_animals': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label='ФИО', max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Телефон', max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name']
        user.last_name = self.cleaned_data['phone'] 
        if commit:
            user.save()
        return user