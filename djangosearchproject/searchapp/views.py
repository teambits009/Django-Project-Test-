from django.shortcuts import render
from .models import Item

# Create your views here.

def search(request):
    return render(request, 'searchapp/search.html')

def results(request):
    query = request.GET.get('query')
    items = Item.objects.filter(name__icontains=query)
    return render(request, 'searchapp/results.html', {'items': items})

