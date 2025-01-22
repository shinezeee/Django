from django.shortcuts import render
from blog.models import Blog
from django.shortcuts import get_object_or_404,render

def blog_list(request):
    blogs = Blog.objects.all()
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