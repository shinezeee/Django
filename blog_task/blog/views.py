from django.contrib.auth.decorators import login_required

from blog.forms import BlogForm
from blog.models import Blog
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') # 최신순으로
    visits = int(request.COOKIES.get('visits', 0)) + 1
    request.session['count'] =request.session.get('count', 0) + 1

    context = {"blogs": blogs}
    response = render(request, 'blog_list.html', context)
    response.set_cookie('visits', visits)
    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {"blog": blog}
    return render(request,'blog_detail.html', context)

@login_required() # 로그인된 유저만 들어울 수 있음
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # 아직 커밋은 안함
        blog.author = request.user # 현재 로그인 된 유저
        blog.save() # 저장
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))
    context = {'form':form}
    return render(request, 'blog_create.html', context)