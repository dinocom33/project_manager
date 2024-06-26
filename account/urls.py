from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/delete_avatar/', views.delete_user_avatar, name='delete_avatar'),
]
