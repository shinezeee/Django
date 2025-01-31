from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.models import Todo


class TodoListView(ListView):
    queryset = Todo.objects.all()
    template_name = 'todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
                )
        return queryset

class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todo_info.html'
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        context = {'todo': self.object.__dict__}
        return context

class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Todo
    fields = ['title','info','start_date','end_date']
    template_name = 'todo_create.html'

    def form_valid(self, form): #폼이 있어야 호출 가능
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cb_todo_info',kwargs={'pk':self.object.pk})

class TodoUpdateView(LoginRequiredMixin,UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ['title','info','start_date','end_date','is_done']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cb_todo_info', kwargs={'pk': self.object.pk})

class TodoDeleteView(LoginRequiredMixin,View):
    def post(self,request,pk):
        todo = get_object_or_404(Todo, pk=pk)
        if todo.user!=request.user and not request.user.is_superuser:
            raise Http404("권한이 없습니다.")
        todo.delete()
        return redirect(reverse_lazy('cb_todo_list'))
