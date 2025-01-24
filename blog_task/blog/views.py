from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from blog.forms import BlogForm
from blog.models import Blog
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') # 최신순으로

    #검색대상 설정
    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
    visits = int(request.COOKIES.get('visits', 0)) + 1
    request.session['count'] =request.session.get('count', 0) + 1
    # 한 페이지당 10개씩 표시
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page') # => 쿼리 스트링 가져옴
    page_object = paginator.get_page(page)
    context = {
        #"blogs": blogs,
        'page_object': page_object,
    }
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

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk,author=request.user)
    form = BlogForm(request.POST or None, instance=blog) # 기초 데이터
    if form.is_valid():
        blog=form.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))
    context = {'blog': blog, 'form': form}
    return render(request,'blog_update.html', context)

@login_required()
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk,author=request.user)
    blog.delete()
    return redirect(reverse('blog_list'))