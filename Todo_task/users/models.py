from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import  BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        # user = self.model(email=self.normalize_email(email), **kwargs)
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)  # 활성화 기본값 추가

        return self.create_user(email, password, **kwargs)

        # user = self.create_user(email, password, **kwargs)
        # user.is_staff = True # 관리자 페이지 접근가능
        # user.is_superuser = True
        # user.is_active = True
        # user.save(using=self._db)
        # return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Django 기본 User 모델과 충돌 방지  (GPT)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )
    objects = UserManager()

    USERNAME_FIELD = 'email' # 이메일을 로그인 아이디로 사용
    REQUIRED_FIELDS = ['name']  # 슈퍼유저 생성시 추가 필수 필드
   # EMAIL_FIELD = 'email' ==> 잘 사용하지 않음
    def __str__(self):
        return self.name

    @property
    def username(self):
        return self.name  # ==>이름을 username으로 반환 -> 호환성