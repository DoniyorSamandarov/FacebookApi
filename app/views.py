from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
import requests

from app.models import User


def confirm(request):
    get_code = request.GET.get('code')
    get_access_token = f"{settings.GET_ACCESS_TOKEN_URL}" \
                       f"client_id={settings.SOCIAL_AUTH_FACEBOOK_KEY}" \
                       f"&redirect_uri={settings.LOCAL_HOST}confirm" \
                       f"&client_secret={settings.SOCIAL_AUTH_FACEBOOK_SECRET}" \
                       f"&code={get_code}&state=for_access_token"
    response = requests.get(get_access_token)
    access_token = response.json().get('access_token')
    get_data = f"{settings.GET_DATA_URL}access_token={access_token}&fields=id,name,email"
    data = requests.get(get_data).json()
    user = User.objects.filter(facebook_id=data.get('id')).first()
    if not user:
        user = User()
        user.facebook_id = data.get('id')
        user.facebook_name = data.get('name')
        user.email = data.get('email', f'{user.facebook_id}@gmail.com')
        user.username = user.email
        user.set_password('admin')
        user.save()
    dj_login(request, user)

    return redirect('/')


def login(request):
    get_code_url = f"{settings.GET_CODE_URL}client_id={settings.SOCIAL_AUTH_FACEBOOK_KEY}" \
                   f"&redirect_uri={settings.LOCAL_HOST}confirm&state=for_code"
    context = {
        'get_code_url': get_code_url
    }
    return render(request, 'templates/login.html', context)


@login_required(login_url='/login')
def main(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'templates/main.html', context)


@login_required(login_url='/login')
def logout(request):
    dj_logout(request)
    return redirect('/')
