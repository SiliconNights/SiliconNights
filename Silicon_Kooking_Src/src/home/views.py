from django.shortcuts import render, HttpResponse

def home_display(request):
    return render(request, 'header.html', {})
