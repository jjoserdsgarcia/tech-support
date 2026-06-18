from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Ticket, Comment, Levels, Entities
from django.contrib import messages

# Create your views here.


def loginscreen(request):
    if request.method == 'GET':
        return render(request, 'techsupport/loginscreen.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainlobby')
        else:
            return render(request, 'techsupport/loginscreen.html', {'error': 'Credenciais inválidas'})


@login_required
def mainlobby(request):
    from .models import Levels, Entities, User, Ticket, Comment


    dashboard_data = {

        'levels_count': Levels.objects.count(),
        'entities_count': Entities.objects.count(),
        'users_count': User.objects.count(),
        'total_tickets': Ticket.objects.count(),
        'open_tickets': Ticket.objects.filter(status='open').count(),
        'closed_tickets': Ticket.objects.filter(status='closed').count(),
        'entity_name': Entities.objects.first().name if Entities.objects.exists() else 'N/A',
        'recent_tickets': Ticket.objects.all().order_by('-created_at')[:5],
        'recent_comments': Comment.objects.all().order_by('-created_at')[:5],
        'authors': {comment.author.username if comment.author else 'Unknown' for comment in Comment.objects.all()},
    }

    return render(request, 'techsupport/mainlobby.html', {'dashboard_data': dashboard_data})


@login_required
def ticketing(request):
    
    if request.method == 'GET':
        return render(request, 'techsupport/ticketing.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        ticket = Ticket.objects.create(title=title, description=description, priority=priority)
        ticket.save()
        messages.success(request, 'Ticket criado com sucesso.')
        return redirect('ticketing')

def registerscreen(request):
   if request.method == 'GET':
        return render(request, 'techsupport/registerscreen.html')
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
            return redirect('techsupport/loginscreen.html')

@login_required
def update_history(request):
    return render(request, 'techsupport/update_history.html')

@login_required
def user_management(request):
    return render(request, 'techsupport/user_management.html')

@login_required
def entity_management(request):
    return render(request, 'techsupport/entity_management.html')

@login_required
def level_management(request):
    return render(request, 'techsupport/level_management.html')


