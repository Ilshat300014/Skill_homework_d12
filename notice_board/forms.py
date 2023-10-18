from django.forms import ModelForm
from .models import Ad
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# class BasicSignupForm(SignupForm):
#     def save(self, request):
#         user = super(BasicSignupForm, self).save(request)
#         basic_group = Group.objects.get_or_create(name='common')[0]
#         basic_group.user_set.add(user)
#         return user

class AdForms(ModelForm):
    class Meta:
        model = Ad
        fields = ['adCategory', 'adTitle', 'adText']
        widgets = {
            'adCategory': forms.Select(attrs={'class': 'form-select'}),
            'adTitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'}),
            'adText': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter article text'})
        }