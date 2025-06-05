from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm, EmailVerificationForm
from .utils import generate_verification_code, send_verification_email
from django.contrib.auth import authenticate
from .models import User
from django.contrib import messages



def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_login')
    else:
        form = UserRegisterForm()

    return render(request, 'user/user_register.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                verification_code = generate_verification_code()

                request.session['verification_code'] = verification_code
                request.session['user_id'] = user.id

                send_verification_email(user.email, verification_code)

                return redirect('verify_code')
            else:
                messages.error(request, 'Неверные учетные данные')
    else:
        form = UserLoginForm()
    return render(request, 'user/user_login.html')


def verify_code(request):
    # Проверяем, есть ли данные в сессии
    if 'verification_code' not in request.session or 'user_id' not in request.session:
        messages.error(request, 'Сначала выполните вход')
        return redirect('user_login')

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            stored_code = request.session['verification_code']

            if entered_code == stored_code:
                # Получаем и авторизуем пользователя
                user = User.objects.get(id=request.session['user_id'])
                login(request, user)

                # Очищаем данные верификации из сессии
                del request.session['verification_code']
                del request.session['user_id']

                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('index')
            else:
                messages.error(request, 'Неверный код подтверждения')
    else:
        form = EmailVerificationForm()

    return render(request, 'user/verify_code.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('user_login')