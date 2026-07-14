"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from techsupport import views
from techsupport.views import loginscreen, mainlobby, registerscreen

urlpatterns = [
    path('', loginscreen, name='home'),
    path('admin/', admin.site.urls),
    
    
    path('login/', loginscreen, name='loginscreen'),

    path('mainlobby/', mainlobby, name='mainlobby'),

    
    path('register/', registerscreen, name='registerscreen'),
    

    path('ticketing/', views.ticketing, name='ticketing'),

    # Painel Staff
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    path("admin-panel/", views.admin_panel, name="admin_panel"),

path("admin-panel/view/<int:ticket_id>/", views.view_ticket, name="view_ticket"),
path("admin-panel/edit/<int:ticket_id>/", views.edit_ticket, name="edit_ticket"),
path("admin-panel/close/<int:ticket_id>/", views.close_ticket, name="close_ticket"),
path("admin-panel/delete/<int:ticket_id>/", views.delete_ticket, name="delete_ticket"),
path("admin-panel/comment/<int:ticket_id>/", views.add_comment, name="add_comment"),
]
