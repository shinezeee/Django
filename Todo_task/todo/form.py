from django import forms

from todo.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description','start_date','end_date']

class TodoUpdateform(forms.ModelForm):
    class Meta:
        model=Todo
        fields = ['title','description','start_date','end_date','is_done']



