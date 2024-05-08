from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

@login_required
def cats_index(request):
    cats = Cat.objects.filter(user=request.user)
    # passing data extremely similar to EJS
    return render(request, 'cats/index.html', {
        'cats': cats
    })

@login_required
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys = Toy
    # Get the toys the cat doesn't have
    id_list = cat.toys.all()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    # making an instance of the FeedingForm class
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat, 
        'feeding_form': FeedingForm,
        'toys': toys_cat_doesnt_have
    })

@login_required
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

@login_required
def assoc_toy(request, pk, toy_pk):
  # Note that you can pass a toy's id instead of the whole toy object
  Cat.objects.get(id=pk).toys.add(toy_pk)
  return redirect('detail', cat_id=pk)

@login_required
def assoc_delete(request, pk, toy_pk):
  Cat.objects.get(id=pk).toys.remove(toy_pk)
  return redirect('detail', cat_id=pk)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
    else:
        error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    # This inherited method is called when a valid cat form is submitted
    def form_valid(self, form):
        # form instance assigning 'user' field to the logged in user 'self.request.user'        
        form.instance.user = self.request.user
        # let the CreateView do its job as usual
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys'
