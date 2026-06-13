from django.db import models


# Create your models here.


class User(models):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True)
    def __str__(self):
        return self.username
    
class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='open')
    priority = models.CharField(max_length=20, default='medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.author} on {self.ticket}'
    
class Levels(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    entities = models.ForeignKey('Entities', on_delete=models.CASCADE, related_name='levels')
    def __str__(self):
        return self.name
    
class Entities(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.name
    