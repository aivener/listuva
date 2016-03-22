from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)

class SignUpForm(forms.Form):
	username = forms.CharField(required=False)
	password = forms.CharField(required=True)
	name = forms.CharField(required=True)
	year = forms.IntegerField(required=True)
	gender = forms.BooleanField(required=True)
