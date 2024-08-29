from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'id':'email',
                                'label':'Email'
                                }))
    password = forms.CharField(max_length=100, 
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'id':'password',
                                }))
    class Meta:
        model = User 
        fields = ['email', 'password']


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, 
                            widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'id':'username',
                                }))
    email = forms.CharField(max_length=100, 
                            widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'id':'email',
                                }))
    
    school = forms.CharField(max_length=100, 
                            widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'id':'school',
                                }))
    

    password1 = forms.CharField(max_length=100, 
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'id':'password',
                                }))
    
    password2 = forms.CharField(max_length=100, 
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'id':'password',
                                }))

    class Meta:
        model = User 
        fields = ['username', 'email', 'location', 'password1','password2']


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'id':'old_password',
                                'label':'Email'
                                }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'id':'password1',
                                'label':'Email'
                                }))
    
    password2 = forms.CharField(max_length=100, 
                            widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'id':'password2',
                                }))
    class Meta:
        model = User 
        fields = ['old_password', 'password1', 'password2']


class DiscussionForm(forms.Form):    
    content = forms.CharField(widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'id':'password1',
                                'label':'content'
                                }))
    
    description = forms.CharField(max_length=100, 
                            widget=forms.Textarea(attrs={
                                'class':'form-control',
                                'id':'password2',
                                'label':'description'
                                }))
    class Meta:
        model = User 
        fields = ['content', 'description']