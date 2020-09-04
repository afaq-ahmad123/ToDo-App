from django.shortcuts import render, redirect, reverse, Http404
from .models import TaskModel
from account.models import User
from account.decorators import login_required
from django.views.generic import ListView, UpdateView
from rest_framework import generics
from .serializer import TaskSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    """Class Based List view to show all the tasks on the home page. It is used instead of home() view function"""

    model = TaskModel
    template_name = 'home/index.html'
    context_object_name = 'tasks'

    extra_context = {
        'i': 1,
    }

    def get_queryset(self):
        """return the Tasks of only logged in user"""
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        return {
            'user': self.request.user,
            'i': 1,
            'tasks': self.model.objects.filter(user=self.request.user)
        }


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
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


class TaskApi(generics.ListCreateAPIView):
    """Api to get the tasks of user with current tokens/Logged in Session"""
    queryset = None
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.queryset = TaskModel.objects.filter(user=self.request.user)
        return super(TaskApi, self).get_queryset()


class TaskUpdateAPI(generics.UpdateAPIView):
    """Getting the Detailed view of task with the specified id"""

    queryset = None
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.queryset = TaskModel.objects.filter(user=self.request.user)
        return super(TaskUpdateAPI, self).get_queryset()


class TaskDeleteAPI(generics.DestroyAPIView):
    queryset = None
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        self.queryset = TaskModel.objects.filter(user=self.request.user)
        return super(TaskDeleteAPI, self).get_queryset()


# @api_view(['GET'])
# def task_list(request):
#     tasks = TaskModel.objects.filter(user=request.user)
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)

@login_required
def delete(request, pk):
    """ This view method is used to delete a specified task from the List """
    task = TaskModel.objects.filter(user=request.user, pk=pk).first()
    if task:
        task.delete()
        task_count = TaskModel.objects.filter(user=request.user).count()
        user = User.objects.get(id=request.user.id)
        user.task_count = task_count
        user.save(update_fields=['task_count'])
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
            task_count = TaskModel.objects.filter(user=request.user).count()
            user = User.objects.get(id=request.user.id)
            user.task_count = task_count
            user.save(update_fields=['task_count'])
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









