from django.urls import path,include
from . import views

urlpatterns = [
    # path('signup/',views.signup,name='signup'),
    # path('login/',views.login,name='login'),
    # path('logout/',views.logout,name='logout'),
    path('login/', views.LoginPage.as_view(), name='signin'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('profile/', views.AccountPage.as_view(), name='account'),
    path('logout/', views.Logout, name='logout'),
]
