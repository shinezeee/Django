from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as django_login


# 현재 Django가 실행되는 환경의 config를 찾아서 import
# 혹시 config나 settings 파일의 이름이 바뀌어도 자동으로 인식
def sign_up(request):
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')
    #
    #
    # print('username', username)
    # print('password1', password1)
    # print('password2', password2)

    # username  중복확인작업
    # 패스워드 정책 맞는지 확인
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == 'POST':  # POST 요청 시
    #     form = UserCreationForm(request.POST)  # 요청된 폼을 form에 받습니다.
    #
    #     # form에 받은 데이터를 검증
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login/')

    # else:  # GET 요청 시 Form 새로 생성
    #     form = UserCreationForm()
# UserCreationForm() 기본적으로 제공하는 가입관련 폼

    context = {
        'form': form,
    }
    return render(request,'registration/signup.html',context)


def login(request):
    form = AuthenticationForm(request,request.POST or None)
    if form.is_valid():
        django_login(request,form.get_user())
        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request,'registration/login.html',context)