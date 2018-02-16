from django.shortcuts import render, HttpResponse
from django.shortcuts import render_to_response


def home_display(request):
	return render(request, 'home/index.html', {})