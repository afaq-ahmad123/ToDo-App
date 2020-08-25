from django.shortcuts import render, redirect, reverse, Http404
from django.contrib.auth.decorators import login_required
from home.models import TaskModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.contrib import messages


class TaskListView(LoginRequiredMixin, ListView):
    """Class Based List view to show all the tasks on the home page. It is used instead of home() view function"""
    model = TaskModel
    template_name = 'home/index.html'
    context_object_name = 'tasks'
    extra_context = {
        'i': 1,
    }

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        print("user id" + str(self.request.user.id))
        return {
            'user': self.request.user,
            'i': 1,
            'tasks': self.model.objects.filter(user=self.request.user)
        }


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Class Based view to update a task. It will use homemodel_form.html template."""
    model = TaskModel
    template_name = 'home/homemodel_form.html'
    fields = ['name', 'complete']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk, user=self.request.user)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            print("object not found")
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_success_url(self):
        return reverse('home-url')



@login_required
def delete(request, pk):
    """ This view method is used to delete a specified task from the List """
    # task = get_object_or_404(TaskModel, pk=pk)
    task = TaskModel.objects.filter(user=request.user, pk=pk).first()
    # print(task.name)
    if task:
        task.delete()
        messages.success(request, "Deleted Successfully")
    else:
        messages.error(request, "Unsuccessful")
    return redirect('/')


@login_required
def complete(request, pk):
    """ This django view method is used to mark a specified task as completed """
    obj = TaskModel.objects.filter(pk=pk).first()
    obj.complete = True
    obj.save()
    messages.success(request, "Marked as Completed")
    return redirect('/')


@login_required
def add_task(request):
    """This django view is used to add a new task in the list"""
    if request.method == "POST":
        name = request.POST['name']
        if name != '':
            obj = TaskModel(name=request.POST['name'], complete=False, user=request.user)
            obj.save()
            messages.success(request, "Task Added Successfully")
        print(request.POST)
    print(TaskModel.objects.filter(user=request.user))
    return redirect(reverse('home-url'))


@login_required
def shortlist(request, i=1):
    """ When a checkbox is checked for a specified view, this view method will be called to
    shortlist the tasks as required """
    i = request.GET.get('i', None)
    print(i)
    results = TaskModel.objects.filter(user=request.user)
    if int(i) == 2:
        results = TaskModel.objects.filter(user=request.user).filter(complete=False)
    elif int(i) == 3:
        results = TaskModel.objects.filter(user=request.user).filter(complete=True)
    print(results)
    context = {
        'tasks': results
    }
    return render(request, 'home/items.html', context)









