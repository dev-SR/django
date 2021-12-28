from django import forms


class DjangoForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    text = forms.CharField(label='Text', widget=forms.Textarea)
