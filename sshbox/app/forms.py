from django import forms


class AccountForm(forms.Form):
	account = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the account name'}))