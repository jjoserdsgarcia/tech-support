from django.contrib import admin

from .models import User, Ticket, Comment, Levels, Entities




# Register your models here.

# admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Levels)
admin.site.register(Entities)
