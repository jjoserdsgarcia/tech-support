from django.shortcuts import render


# Create your views here.


def loginscreen(request):
    return render(request, 'techsupport/loginscreen.html')
