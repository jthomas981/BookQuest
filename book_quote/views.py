from django.http import HttpResponse
from django.shortcuts import render

from book_quote.tasks import reload_website

reload_website()

def homepage(request):
    return render(request, 'homepage.html')