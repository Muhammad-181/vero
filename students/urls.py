from django.urls import path
from . import views


app_name = "students"


urlpatterns = [
    path('', views.index, name="index"),
    path('get_departments/', views.get_departments, name='get_departments'),
    path('login/', views.login_user, name="login_user"),
    path('register/', views.register_user, name="register"),
    path('reset-info/', views.edit_details, name="reset-info"),
    path('reset-image/', views.edit_profilepicture, name="reset-image"),
    path('reset-password/', views.forget_password, name="forget_password"),
    path('change-password/', views.change_password, name="change-password"),
    path('logout/', views.logout_user, name='logout_user'),
]