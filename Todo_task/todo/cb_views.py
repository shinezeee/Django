from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.form import CommentForm, TodoForm, TodoUpdateForm
from todo.models import Todo, Comment

# 할 일 목록
class TodoListView(LoginRequiredMixin,ListView):
    queryset = Todo.objects.all()
    template_name = 'todo/todo_list.html'
    paginate_by = 10  #페이지네이션
    ordering = ['-created_at'] #최신순 정렬

    def get_queryset(self):
        # 기본 적으로 로그인한 사용자의 할 일만 표시
        queryset = Todo.objects.filter(user=self.request.user)
        # 슈퍼유저는 모든 할일 조회
        if self.request.user.is_superuser:
            queryset = Todo.objects.all()
        # 검색기능 ( q = 검색어 )
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(   # 검색
                Q(title__icontains=q) |
                Q(info__icontains=q)
                )
        return queryset

# 할 일 상세보기 (댓글포함)
class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   #기존 컨텍스트 유지
        comments = self.object.comments.order_by('-created_at') # 댓글 최신순 정렬
        paginator = Paginator(comments,5)
        context.update({ # 기존 컨택스트에 댓글을 추가해서 표시
                   'comment_form': CommentForm(),
                   'page_obj':paginator.get_page(self.request.GET.get('page')) #현재 페이지의 댓글 추가
        })
        return context

# 할 일 추가
class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Todo
    template_name = 'todo/todo_create.html'
    form_class = TodoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect('cb_todo_info', pk=self.object.pk)


    def get_success_url(self):
        if self.object and self.object.pk:
            return reverse_lazy('cb_todo_info', kwargs={'pk': self.object.pk})
        return reverse_lazy('cb_todo_list')  # 오류 방지를 위해 기본적으로 리스트 페이지로 이동

# 할 일 수정
class TodoUpdateView(LoginRequiredMixin,UpdateView):
    model = Todo
    template_name = 'todo/todo_update.html'
    form_class = TodoUpdateForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cb_todo_info', kwargs={'pk': self.object.pk})

# 할 일 삭제 (템플릿 없이 바로 삭제)
class TodoDeleteView(LoginRequiredMixin,View):
    def post(self,request,pk):
        todo = get_object_or_404(Todo, pk=pk)
        if todo.user!=request.user and not request.user.is_superuser:
            raise Http404("권한이 없습니다.")
        todo.delete()
        return redirect(reverse_lazy('cb_todo_list'))

# 댓글 추가
class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['message']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = get_object_or_404(Todo, id = self.kwargs["todo_id"])
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cb_todo_info', kwargs={'pk': self.kwargs['todo_id']})

# 댓글 수정
class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['message']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('권한이 없습니다.')
        return obj

    def get_success_url(self):
        return reverse_lazy('cb_todo_info', kwargs={'pk' : self.object.todo.id})

# 댓글 삭제
class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('권한이 없습니다.')
        return obj
    def get_success_url(self):
        return reverse_lazy('cb_todo_info', kwargs={'pk' : self.object.todo.id})
