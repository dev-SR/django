from django import forms
from .models import ReviewModel

class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        # fields = ['username', 'review_text', 'rating']
        fields = '__all__'
        # exclude = ['username']
        labels = {
            'username': 'Your Username',
            'review_text': 'Your Review',
            'rating': 'Your Rating'
        }
        error_messages = {
            'username': {
                'required': 'Please enter your username',
                'max_length': 'Please enter a username less than 10 characters',
            },
            'review_text': {
                'required': 'Please enter your review',
                'max_length': 'Please enter a review less than 200 characters',
            },
            'rating': {
                'required': 'Please enter your rating',
                'min_value': 'Please enter a rating greater than 1',
                'max_value': 'Please enter a rating less than 5',
            }
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'cols': 40, 'rows': 15})
        }
