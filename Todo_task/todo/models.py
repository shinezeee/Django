import re
import requests

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
#from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from pathlib import Path
from io import BytesIO
from config import settings

# Create your models here.

User = get_user_model()

class Todo(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 로그인유저 확인
    title = models.CharField(max_length=50) # 제목
    info = models.TextField() # 할일 설명
    start_date = models.DateField() # 시작 날짜
    end_date = models.DateField() # 끝나는 날짜
    is_done = models.BooleanField(default=False) # 완료 여부
    thumbnail = models.ImageField(
        upload_to = 'thumbnails/',
        default = 'thumbnails/default.png',
        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정 날짜

    # completed_image = models.ImageField(upload_to='todo/completed_images', null=True, blank=True)
    # 이미지 저장은 안할거임

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        """✅ 섬네일이 있으면 반환, 없으면 기본 썸네일 반환"""
        if self.thumbnail and self.thumbnail.name:  # 파일이 있는지 확인
            return f"{settings.MEDIA_URL}{self.thumbnail.name}"
        return f"{settings.MEDIA_URL}thumbnails/default.png"

    def extract_first_image(self):
        """Summernote 내용에서 첫 번째 이미지 URL을 추출"""
        img_match = re.search(r'<img.*?src="(.*?)"', self.info)
        if img_match:
            img_url = img_match.group(1)
            # 만약 URL이 상대 경로라면 절대 경로로 변경
            if not img_url.startswith("http"):
                img_url = f"{settings.MEDIA_URL.lstrip('/')}{img_url.lstrip('/')}"
            return img_url
        return None

    def save(self, *args, **kwargs):
        """📌 Summernote에서 첫 번째 이미지를 가져와 썸네일로 저장"""
        if not self.thumbnail or self.thumbnail.name == "thumbnails/default.png":  # 썸네일이 기본 이미지일 때만 실행
            first_img_url = self.extract_first_image()
            print(f"📌 첫 번째 이미지 URL: {first_img_url}")  # 👉 Debugging 로그 추가

            if first_img_url:
                if first_img_url.startswith("http"):  # 🔹 외부 URL 이미지라면 다운로드 후 저장
                    try:
                        response = requests.get(first_img_url, stream=True)
                        if response.status_code == 200:
                            img_name = first_img_url.split("/")[-1].split("?")[0]  # URL에서 파일명 추출
                            temp_img = BytesIO(response.content)

                            # 이미지 열기 및 썸네일 생성
                            image = Image.open(temp_img)
                            image.thumbnail((100, 100))

                            temp_thumb = BytesIO()
                            image.save(temp_thumb, format="PNG")
                            temp_thumb.seek(0)

                            # 저장
                            self.thumbnail.save(f"thumb_{img_name}", ContentFile(temp_thumb.read()), save=False)
                            temp_thumb.close()
                            print(f"✅ 썸네일 저장 성공: {self.thumbnail.name}")  # 👉 Debugging 로그 추가
                    except Exception as e:
                        print(f"❌ 외부 이미지 다운로드 실패: {e}")
                else:
                    # 내부 media 폴더의 이미지라면 기존 로직 그대로 적용
                    media_path = first_img_url.replace(settings.MEDIA_URL, "")  # /media/ 제거
                    print(f"📌 변환된 이미지 경로: {media_path}")  # 👉 Debugging 로그 추가

                    if default_storage.exists(media_path):  # 파일이 존재하는지 확인
                        try:
                            with default_storage.open(media_path, "rb") as img_file:
                                img_name = media_path.split("/")[-1]

                                # 이미지 열기 및 썸네일 생성
                                image = Image.open(img_file)
                                image.thumbnail((100, 100))

                                temp_thumb = BytesIO()
                                image.save(temp_thumb, format="PNG")
                                temp_thumb.seek(0)

                                # 저장
                                self.thumbnail.save(f"thumb_{img_name}", ContentFile(temp_thumb.read()), save=False)
                                temp_thumb.close()
                                print(f"✅ 썸네일 저장 성공: {self.thumbnail.name}")  # 👉 Debugging 로그 추가
                        except Exception as e:
                            print(f"❌ 썸네일 생성 실패: {e}")

        super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     """ Summernote 이미지 중 첫 번째 이미지를 썸네일로 저장 """
    #     if not self.completed_image:
    #         # Summernote 내용에서 이미지 태그 추출
    #         match = re.search(r'<img.*?src="(.*?)"', self.info)
    #         if match:
    #             image_url = match.group(1)  # 첫 번째 이미지 URL
    #
    #             from django.contrib.sites import requests
    #             image_response = requests.get(image_url)
    #
    #             if image_response.status_code == 200:
    #                 image_name = Path(image_url).name
    #                 self.completed_image.save(image_name, ContentFile(image_response.content), save=False)
    #
    #     super().save(*args, **kwargs)
    #
    #     # 썸네일 생성
    #     if self.completed_image and not self.thumbnail:
    #         image = Image.open(self.completed_image)
    #         image.thumbnail((100, 100))
    #
    #         image_path = Path(self.completed_image.name)
    #         thumbnail_name = f'{image_path.stem}_thumbnail{image_path.suffix}'
    #
    #         temp_thumb = BytesIO()
    #         image.save(temp_thumb, format=image.format)
    #         temp_thumb.seek(0)
    #
    #         self.thumbnail.save(thumbnail_name, temp_thumb, save=False)
    #
    #         temp_thumb.close()
    #         super().save(*args, **kwargs)

class Comment(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.message}'