from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def contacts(request):
    return render(request, 'contacts.html')


def alarm(request):
    return render(request, 'alarm.html')


def location(request):
    return render(request, 'location.html')

