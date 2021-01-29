from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='signin'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('profile/', views.AccountPage.as_view(), name='account'),
    path('logout/', views.Logout, name='logout'),
    path('change-password/', views.ChangePasswordPage.as_view(), name='change_password'),
    path('reset-password/', views.ResetPasswordFormPage.as_view(), name='password_reset'),
    # path('password_reset/', views.ResetPasswordStart.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.ResetPasswordVerify.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
