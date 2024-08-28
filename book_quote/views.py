from django.http import HttpResponse
from django.shortcuts import render

from BookQuest.tasks import reload_website

reload_website()

def homepage(request):
    return render(request, 'homepage.html')