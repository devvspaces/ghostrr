from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import logout,authenticate
from django.contrib.auth import login
from django.views.generic import FormView, TemplateView

from .forms import UserRegisterForm, LoginForm


# Create your views here.
# def signup(request):
#     return render (request,'accounts/signup.html')

# def login(request):
#     return render (request,'accounts/login.html')

# def logout(request):
#     #need to route to home & logout from user
#     return render (request,'accounts/signup.html')


class LoginPage(FormView):
    template_name = 'accounts/signin.html'
    extra_context = {
        'title': 'Login',
    }
    form_class = LoginForm

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context
        context['form'] = self.get_form_class()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        form = self.get_form_class()
        form = form(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('index_page')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


class RegisterPage(FormView):
    template_name = 'accounts/register.html'
    extra_context = {
        'title': 'Register',
    }
    form_class = UserRegisterForm

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context
        context['form'] = self.get_form_class()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        form = self.get_form_class()
        form = form(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'You account have been successfully created')
            return redirect('signin')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


def Logout(request):
	logout(request)
	return redirect('index_page')