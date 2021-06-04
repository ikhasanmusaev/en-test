from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'tag': 'index'})


def about(request):
    return render(request, 'about.html', {'tag': 'about'})


def contact(request):
    return render(request, 'contact.html', {'tag': 'contact'})


def our_team(request):
    return render(request, 'team.html')


def events(request):
    return render(request, 'events.html')
