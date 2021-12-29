from django.db import models

# Create your models here.


class ReviewModel(models.Model):
    username = models.CharField(max_length=100)
    review_text = models.CharField(max_length=500)
    rating = models.IntegerField()
