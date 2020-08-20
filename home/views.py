from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from home.models import HomeModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from .forms import EditForm
from django.contrib import messages


class TaskListView(LoginRequiredMixin, ListView):
    """Class Based List view to show all the tasks on the home page. It is used instead of home() view function"""
    model = HomeModel
    template_name = 'home/index.html'
    context_object_name = 'tasks'
    extra_context = {
        'i': 1
    }

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Class Based view to update a task"""
    model = HomeModel
    fields = ['name', 'complete']

    def get_success_url(self):
        return reverse('home-url')


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
    if task:
        task.delete()
        messages.success(request, "Deleted Successfully")
    else:
        messages.error(request, "Unsuccessful")
    return redirect('/')


def complete(request, pk):
    """ This django view method is used to mark a specified task as completed """
    obj = HomeModel.objects.filter(pk=pk).first()
    obj.complete = True
    obj.save()
    messages.success(request, "Marked as Completed")
    return redirect('/')


def add_task(request):
    """This django view is used to add a new task in the list"""
    if request.method == "POST":
        name = request.POST['name']
        if name != '':
            obj = HomeModel(name=request.POST['name'], complete=False, user=request.user)
            obj.save()
            messages.success(request, "Task Added Successfully")
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


def edit_task(request, pk=None):
    task = get_object_or_404(HomeModel, pk)
    if request.method == "POST":
        obj = EditForm(request.POST or None, instance=task)
        if obj.is_valid():
            obj.save()
            return HttpResponseRedirect(task.get_absolute_url())










