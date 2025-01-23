from django.db import models

# Create your models here.

class Todo(models.Model) :
    title = models.CharField(max_length=50) # 제목
    description = models.TextField() # 할일 설명
    start_date = models.DateField() # 시작 날짜
    end_date = models.DateField() # 끝나는 날짜
    is_done = models.BooleanField(default=False) # 완료 여부
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜


    def __str__(self):
        return self.title
