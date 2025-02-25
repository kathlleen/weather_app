from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'title': 'Погода на сегодня'
    }
    return render(request, 'index.html', context)

def query(request):
    context = {
        'title': 'Query history'
    }
    return render(request, 'query.html', context)

