from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def bingo(request):
    return render(request, 'bingo.html', {})

def bmi(request):
    return render(request, 'bmi.html', {})