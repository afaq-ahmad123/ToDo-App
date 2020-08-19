from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from home.models import HomeModel


@login_required
def home(request):
    """ This is the main Home Page view to show all the tasks of logged in user """

    if request.user.is_authenticated:
        username = request.user.username
    context = {
        'i': 1,
        'user': username,
        'tasks': HomeModel.objects.filter(user=request.user)
    }
    return render(request, 'home/index.html', context)


def delete(request, pk):
    """ This view method is used to delete a specified task from the List """
    task = get_object_or_404(HomeModel, pk=pk)
    print(task.name)
    task.delete()
    return redirect('/')


def complete(request, pk):
    """ This django view method is used to mark a specified task as completed """
    obj = HomeModel.objects.filter(pk=pk).first()
    obj.complete = True
    obj.save()
    return redirect('/')


def add_task(request):
    """This django view is used to add a new task in the list"""
    if request.method == "POST":
        name = request.POST['name']
        if name != '':
            obj = HomeModel(name=request.POST['name'], complete=False, user=request.user)
            obj.save()
        print(request.POST)
    print(HomeModel.objects.filter(user=request.user))
    return redirect(reverse('home-url'))


def shortlist(request, i=1):
    """ When a checkbox is checked for a specified view, this view method will be called to
    shortlist the tasks as required """
    i = request.GET.get('i', None)
    print(i)
    results = HomeModel.objects.filter(user=request.user)
    if int(i) == 2:
        results = HomeModel.objects.filter(user=request.user).filter(complete=False)
    elif int(i) == 3:
        results = HomeModel.objects.filter(user=request.user).filter(complete=True)
    print(results)
    context = {
        'tasks': results
    }
    return render(request, 'home/items.html', context)







