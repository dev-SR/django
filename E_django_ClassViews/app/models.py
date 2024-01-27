from django.db import models
# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=200, blank=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PhotoModel(models.Model):
    caption = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='images', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.caption
