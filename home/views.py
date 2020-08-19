from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from .forms import HomeForm
from django.shortcuts import get_object_or_404
from home.models import HomeModel


@login_required
def home(request):
    if request.method == 'POST':
        print(request.POST)
    form = HomeForm(request.POST or None)
    print("Model Data")
    print(HomeModel.objects.filter(user=request.user))
    if request.user.is_authenticated:
        username = request.user.username
    context = {
        'form': form,
        'user': username,
        'tasks': HomeModel.objects.filter(user=request.user)
    }
    return render(request, 'home/index.html', context)


def delete(request, pk):
    task = get_object_or_404(HomeModel, pk=pk)
    print(task.name)
    task.delete()
    return redirect('/')


def complete(request, pk):
    obj = HomeModel.objects.filter(pk=pk).first()
    obj.complete = True
    obj.save()
    return redirect('/')


def add_task(request):
    print("In add")
    if request.method == "POST":
        obj = HomeModel(name=request.POST['name'], complete=False, user=request.user)
        obj.save()
        print(request.POST)

    return redirect('/')




