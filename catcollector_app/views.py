from django.shortcuts import render
# from django.http import HttpResponse

# Add this cats list below the imports
cats = [
  {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
  {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
]

# Create your views here.
def home(request):
    # res.send('hello') in express
    # return HttpResponse('hello')
    return render(request, 'cats/home.html')

def about(request):
    return render(request, 'cats/about.html')

def cats_index(request):
    # passing data extremely similar to EJS
    return render(request, 'cats/index.html', {
        'cats': cats
    })
