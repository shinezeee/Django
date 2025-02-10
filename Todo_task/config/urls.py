"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from todo import cb_views
from todo.views import todo_list, todo_info, todo_create, todo_update, todo_delete, todo_home
from users import views as user_views
from todo.views import custom_404_view
from django.conf import settings
from django.conf.urls.static import static

handler404 = "todo.views.custom_404_view"

urlpatterns = [
    # FBV
    path('',todo_home, name='todo_home'),
    path("todo/", todo_list, name="todo_list"),
    path("todo/create/",todo_create, name="todo_create"),
    path("todo/<int:todo_id>/",todo_info, name="todo_info"),
    path("todo/<int:todo_id>/update",todo_update , name="todo_update"),
    path("todo/<int:todo_id>/delete", todo_delete, name="todo_delete"),

    path("admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    # path("signup/", user_views.signup, name="signup"),
    # path("login/", user_views.login, name="login"),
    # path("logout/",user_views.logout, name="logout"),
    path('summernote/', include('django_summernote.urls')),
    #CBV include
    path('cbv/',include('todo.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)