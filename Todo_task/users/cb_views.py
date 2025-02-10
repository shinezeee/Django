from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import SignupForm, LoginForm
from utils.email import send_email

User = get_user_model()

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save()
        user.is_active = False  # 이메일 인증 전까지 비활성화
        user.save()
        # 이메일 인증링크 생성
        signer = TimestampSigner() # 암호화
        signed_user_email = signer.sign(user.email)
        url = f"{self.request.scheme}://{self.request.META['HTTP_HOST']}/users/verify/?code={signed_user_email}"
        subject = f"[Todo List] {user.email} 님의 이메일 인증 링크 입니다."
        message = f"""
        아래의 링크를 클릭하여 이메일 인증을 완료해주세요.\n\n
        {url}\n\n
        """
        send_email(subject=subject, message=message, to_email=user.email)
        return render(self.request, 'registration/signup_success.html')


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("cb_todo_list") # 로그인 성공시 리스트
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

def verify_email(request):
    code = request.GET.get('code') # 사용자가 이메일에서 클릭한 코드 가져와
    # 없다면 실패 페이지
    if not code:
        return render(request, 'registration/verify_failed.html')
    signer = TimestampSigner() # 서명검증객체
    try :
        user_email = signer.unsign(code,max_age=60*5) #5분 내 인증
        user = get_object_or_404(User, email=user_email) # 이메일 가진 사용자 찾기
        user.is_active =True # 활성화
        user.save() #저장
        return render(request, 'registration/verify_success.html') # 인증성공

    except (TypeError,SignatureExpired):
        return render(request,'registration/verify_failed.html')
