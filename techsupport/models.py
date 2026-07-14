from django.db import models
from django.contrib.auth.models import User




# Create your models here.


# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     is_admin = models.BooleanField(default=False)
#     email = models.EmailField(max_length=254, unique=True)
#     def __str__(self):
#         return self.username
    
    
    
class Priority(models.TextChoices):
    BAIXA = "Baixa", "Baixa"
    MEDIA = "Média", "Média"
    ALTA = "Alta", "Alta"
    CRITICA = "Crítica", "Crítica"
    

class Priority(models.TextChoices):
    BAIXA = "Baixa", "Baixa"
    MEDIA = "Média", "Média"
    ALTA = "Alta", "Alta"
    CRITICA = "Crítica", "Crítica"


class Status(models.TextChoices):
    ABERTO = "ABERTO", "Aberto"
    EM_ANDAMENTO = "EM ANDAMENTO", "Em Andamento"
    FECHADO = "FECHADO", "Fechado"
    CANCELADO = "CANCELADO", "Cancelado"

class Ticket(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTO
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIA
    )

    # Quem criou
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    # Quem está responsável
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets"
    )

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.ticket}"

  



class SystemLog(models.Model):
    message = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message
    
    
class Levels(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    room_entities = models.ForeignKey('Entities', related_name='levels', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Entities(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    room_levels = models.ForeignKey('Levels', related_name='entities', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    

