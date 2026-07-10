from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Levels, Entities, User, Ticket, Comment
from django.contrib import messages
from .decorators import staff_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

# Armazena tentativas de login
# Armazena tentativas de login
login_attempts = {}

def loginscreen(request):

    if request.method == 'GET':
        return render(request, 'techsupport/loginscreen.html')

    elif request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print(user)

        if user is not None:

            login(request, user)

            # Se for Staff/Admin
            if user.is_staff:
                return redirect('admin_panel')

            # Usuário comum
            return redirect('mainlobby')

        # Login inválido
        return render(
            request,
            'techsupport/loginscreen.html',
            {
                'error': 'Credenciais inválidas'
            }
        )
  


@login_required
def mainlobby(request):
    


    dashboard_data = {

        'levels_count': Levels.objects.count(),
        'entities_count': Entities.objects.count(),
        'users_count': User.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'open_tickets': Ticket.objects.filter(status='Aberto').count(),
        'closed_tickets': Ticket.objects.filter(status='Fechado').count(),
        'pending_tickets': Ticket.objects.filter(status='Em Andamento').count(),
        'cancelled_tickets': Ticket.objects.filter(status='Cancelado').count(),
        'entity_name': Entities.objects.first().name if Entities.objects.exists() else 'N/A',
        'recent_tickets': Ticket.objects.prefetch_related('comments').all(),
        'authors': {comment.author.username if comment.author else 'Unknown' for comment in Comment.objects.all()},
    }
    return render(request, 'techsupport/mainlobby.html', {'dashboard_data': dashboard_data})

@login_required
def ticketing(request):

    print("ticketing")
    


    dashboard_data = {

        'levels_count': Levels.objects.count(),
        'entities_count': Entities.objects.count(),
        'users_count': User.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'open_tickets': Ticket.objects.filter(status='ABERTO').count(),
        'closed_tickets': Ticket.objects.filter(status='FECHADO').count(),
        'pending_tickets': Ticket.objects.filter(status='EM ANDAMENTO').count(),
        'cancelled_tickets': Ticket.objects.filter(status='CANCELADO').count(),
        'entity_name': Entities.objects.first().name if Entities.objects.exists() else 'N/A',
        'recent_tickets': Ticket.objects.prefetch_related('comments').all(),
        'authors': {comment.author.username if comment.author else 'Unknown' for comment in Comment.objects.all()},
    }

    
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        ticket = Ticket.objects.create(title=title, description=description, priority=priority)
        ticket.save()
        messages.success(request, 'Ticket criado com sucesso.')

        return redirect('ticketing')
       
    print(dashboard_data)
    return render(request, 'techsupport/ticketing.html', {'dashboard_data': dashboard_data})




def registerscreen(request):
   if request.method == 'GET':
        
        


        dashboard_data = {

        'levels_count': Levels.objects.count(),
        'entities_count': Entities.objects.count(),
        'users_count': User.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'open_tickets': Ticket.objects.filter(status='Aberto').count(),
        'closed_tickets': Ticket.objects.filter(status='Fechado').count(),
        'pending_tickets': Ticket.objects.filter(status='Em Andamento').count(),
        'cancelled_tickets': Ticket.objects.filter(status='Cancelado').count(),
        'entity_name': Entities.objects.first().name if Entities.objects.exists() else 'N/A',
        'recent_tickets': Ticket.objects.prefetch_related('comments').all(),
        'authors': {comment.author.username if comment.author else 'Unknown' for comment in Comment.objects.all()},
        }

        return render(request, 'techsupport/registerscreen.html', {"dashboard_data": dashboard_data})
   
   elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username já existe.')
            return render(request, 'techsupport/registerscreen.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já registrado.')
            return render(request, 'techsupport/registerscreen.html')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Conta criada com sucesso. Faça login para continuar.')
            return redirect('/login/')
        

       

@staff_member_required
def admin_panel(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        Ticket.objects.create(
            title=title,
            description=description,
            priority=priority
        )

        messages.success(request, "Ticket criado com sucesso!")

        return redirect("admin_panel")

    dashboard_data = {
        'levels_count': Levels.objects.count(),
        'entities_count': Entities.objects.count(),
        'users_count': User.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'open_tickets': Ticket.objects.filter(status='ABERTO').count(),
        'closed_tickets': Ticket.objects.filter(status='FECHADO').count(),
        'pending_tickets': Ticket.objects.filter(status='EM ANDAMENTO').count(),
        'recent_tickets': Ticket.objects.order_by('-id'),
    }

    return render(request, "techsupport/admin.html", {
        "dashboard_data": dashboard_data,
        "tickets": dashboard_data["recent_tickets"],
        "users": User.objects.all(),
        "total_tickets": dashboard_data["total_tickets"],
        "open_tickets": dashboard_data["open_tickets"],
        "pending_tickets": dashboard_data["pending_tickets"],
        "closed_tickets": dashboard_data["closed_tickets"],
        "users_count": dashboard_data["users_count"],
    })


from django.shortcuts import get_object_or_404

@staff_member_required
def view_ticket(request, ticket_id):
    return redirect("admin_panel")


@staff_member_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        ticket.title = request.POST.get("title")
        ticket.description = request.POST.get("description")
        ticket.priority = request.POST.get("priority")
        ticket.status = request.POST.get("status")
        ticket.save()

        messages.success(request, "Ticket atualizado com sucesso!")
        return redirect("admin_panel")
    


@staff_member_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = "FECHADO"
    ticket.save()

    messages.success(request, "Ticket fechado com sucesso.")
    return redirect("admin_panel")


@staff_member_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()

    messages.success(request, "Ticket excluído.")
    return redirect("admin_panel")





