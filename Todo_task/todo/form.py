from django import forms

from todo.models import Todo, Comment
from django_summernote.widgets import SummernoteWidget


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'info','start_date','end_date']
        widgets = {
            'info': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),}

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields = ['title','info','start_date','end_date','is_done']
        widgets = {
            'info': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'btn-check', 'id': 'toggle-is-done'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message': '내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'cols': 50,
                'class': 'form-control',
                'placeholder': '댓글을 남겨보세요.'
                }),
        }

