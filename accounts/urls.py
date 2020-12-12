from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='accounts/password_form.html'),name='password'),
    path('view_profile/',views.view_profile, name="view_profile"),
    path('update/<int:pk>/',views.ProfileUpdate.as_view(),name='update'),
    path('update_picture/<int:pk>/',views.PictureUpdate.as_view(), name="update_picture")
]
