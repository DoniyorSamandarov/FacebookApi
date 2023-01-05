from django.urls import path
from .views import login, main, confirm, logout

urlpatterns = [
    path('', main, name='main'),
    path('login/', login, name='login'),
    path('confirm/', confirm, name='confirm'),
    path('logout/', logout, name='logout')
]
