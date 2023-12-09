from django.db import models
from django.urls import reverse

class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default='')
    # Here is a diff with the book. on_delete is required,
    # and models.CASCADE is the default
    # So item is required to have text and be associatd with a list
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    
