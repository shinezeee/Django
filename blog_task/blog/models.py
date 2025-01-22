from django.db import models

# Create your models here.

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('daily','일상'),
        ('travel','여행'),
        ('hobby','취미'),
        ('cook','요리')
    )

    category = models.CharField('카테고리',max_length=20,choices=CATEGORY_CHOICES)
    title = models.CharField('제목',max_length=100)
    content = models.CharField('본문',max_length=2000)

    created_at = models.DateTimeField('작성일자',auto_now_add=True)
    updated_at = models.DateTimeField('작성일자',auto_now=True)


    # 제목 노출되는 형식 설정 [카테고리] 제목은 최대 10자까지 노출
    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'