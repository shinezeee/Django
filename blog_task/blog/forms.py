from django import forms
from blog.models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content') # 전체는 __all__

