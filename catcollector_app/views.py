from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat
from .forms import FeedingForm
# Add this cats list below the imports
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
# ]

# Create your views here.
def home(request):
    # res.send('hello') in express
    # return HttpResponse('hello')
    return render(request, 'cats/home.html')

def about(request):
    return render(request, 'cats/about.html')

def cats_index(request):
    cats = Cat.objects.all()
    # passing data extremely similar to EJS
    return render(request, 'cats/index.html', {
        'cats': cats
    })

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # making an instance of the FeedingForm class
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat, 'feeding_form': FeedingForm
    })

def add_feeding(request, pk):
    # create a ModelForm instance with POST data
    # this is like req.body in express
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # dont save the form until it has our cat_id assigned
        new_feeding = form.save(commit=False)
        # date, meal, cat --> cat_id is django magic
        new_feeding.cat_id = pk
        new_feeding.save()
    return redirect('detail', cat_id=pk)


class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'
