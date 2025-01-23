from typing import Any

from django.db.models import QuerySet
from django.shortcuts import render
from django.http import Http404
from todo.models import Todo


# Create your views here.

def todo_list (request):
    todo_list = Todo.objects.all().values_list('id','title')
    result  = [{'id' : todo[0],'title': todo[1] }for todo in todo_list]

    return render(request,'todo_list.html',{'data':result})

def todo_info(request,todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            'title' : todo.title,
            'description' : todo.description,
            'start_date' : todo.start_date,
            'end_date' : todo.end_date,
            'is_done' : todo.is_done,
        }
        return render(request,'todo_info.html',{'data':info})
    except Todo.DoesNotExist:
        raise Http404 ("Todo does not exist")