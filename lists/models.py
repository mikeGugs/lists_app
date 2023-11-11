from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    # Here is a diff with the book. on_delete is required,
    # and models.CASCADE is the default
    # So item is required to have text and be associatd with a list
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    
