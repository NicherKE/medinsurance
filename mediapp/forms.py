
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Prediction, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['age', 'gender', 'bmi', 'children', 'smoker', 'region']
        
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0 or age > 120:
            raise forms.ValidationError("Please enter a valid age between 0 and 120.")
        return age
        
    def clean_bmi(self):
        bmi = self.cleaned_data['bmi']
        if bmi < 10 or bmi > 50:
            raise forms.ValidationError("Please enter a valid BMI between 10 and 50.")
        return bmi
        
    def clean_children(self):
        children = self.cleaned_data['children']
        if children < 0:
            raise forms.ValidationError("Number of children cannot be negative.")
        return children

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'phone']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
