from django import forms


class ReviewForm(forms.Form):
    username = forms.CharField(label="Your Username", max_length=10, error_messages={
        'required': 'Please enter your username',
        'max_length': 'Please enter a username less than 10 characters',
    }, required=False)
    review_text = forms.CharField(
        label="Your Review", max_length=200, widget=forms.Textarea)
    rating = forms.IntegerField(label="Your Rating", min_value=1, max_value=5)
