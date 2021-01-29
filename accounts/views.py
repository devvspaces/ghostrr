from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib import auth, messages
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login
from django.views.generic import FormView, TemplateView

from .forms import (UserRegisterForm, LoginForm,
    UserUpdateFormPage, UserChangePasswordForm,
    ResetPasswordValidateEmailForm, ForgetPasswordForm)
from .models import User
from .tokens import acount_confirm_token



class ResetPasswordVerify(FormView):
    template_name = 'accounts/reset_password_page.html'
    extra_context = {
        'title': 'Reset your password',
    }
    form_class = ForgetPasswordForm

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context
        context['form'] = self.get_form_class()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Get uidb4 and token from kwargs
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        uid=force_text(urlsafe_base64_decode(uidb64))
        user=get_object_or_404(User, pk=uid)

        if acount_confirm_token.check_token(user,token):
            messages.success(request,'You can now change your password here')
        else:
            messages.warning(request, 'This password reset link is already invalid. Get a new link mailed to you with the change password button on your accounts page')
            return redirect('signin')

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        # Get uidb4 from kwargs and get the user instance
        uidb64 = self.kwargs.get('uidb64')
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=get_object_or_404(User, pk=uid)

        # Get request.POST and copy
        default_post = request.POST.copy()
        default_post['user_pk'] = user.pk

        form = self.get_form_class()
        form = form(default_post)

        if form.is_valid():
            form.save()
            messages.success(request, 'You password has been successfully changed, now login with your new password')
            return redirect('signin')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


def verification_message(request, user):
	site=get_current_site(request)
	uid=urlsafe_base64_encode(force_bytes(user.pk))
	token=acount_confirm_token.make_token(user)
	message=render_to_string("accounts/password_email.html",{
		"user": user.username,
		"uid": uid,
		"token": token,
		"domain": site.domain,
		'from': settings.DEFAULT_FROM_EMAIL
	})
	return message


class ResetPasswordFormPage(FormView):
    template_name = 'accounts/reset_password_form.html'
    extra_context = {
        'title': 'Reset Password',
    }
    form_class = ResetPasswordValidateEmailForm

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
            user = get_object_or_404(User, email=email)

            # Send the reset link to user
            subject = "Ghostrr Password Reset"
            message = verification_message(request, user)
            sent=user.email_user(subject,message)

            messages.success(request, 'We sent your password reset link to your email, click on the link to reset your password')

            return redirect('signin')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


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
        # Redirect to create blogs is user is logged in
        if request.user.is_authenticated:
            messages.success(request, 'Logout first')
            return redirect('account')
            
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        form = self.get_form_class()
        form = form(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = get_object_or_404(User, email=email)
            # user = authenticate(request, username=email, password=password)
            # print(user)
            if user:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
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
        # Redirect to create blogs is user is logged in
        if request.user.is_authenticated:
            return redirect('create_blog')

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


class AccountPage(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile.html'
    extra_context = {
        'title': 'Account',
    }
    form_class = UserUpdateFormPage

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context
        form = self.get_form_class()

        default_post = self.request.POST.copy()
        default_post['username'] = self.request.user.username
        default_post['email'] = self.request.user.email
        default_post['pk'] = self.request.user.pk

        form = form(default_post)

        context['form'] = form

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        form = self.get_form_class()
        default_post = request.POST.copy()
        default_post['pk'] = request.user.pk
        form = form(default_post)

        if form.is_valid():
            # Get the user from request
            user = request.user

            # Set new values
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user = user.save()
            messages.success(request, 'You account have been successfully updated')
            return redirect('account')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


class ChangePasswordPage(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_password.html'
    extra_context = {
        'title': 'Change your password',
    }
    form_class = UserChangePasswordForm

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context
        context['form'] = self.get_form_class()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        # Copy the request.POST data to add user_pk
        default_post = request.POST.copy()
        default_post['user_pk'] = request.user.pk

        form = self.get_form_class()
        form = form(default_post)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'You have successfully changed your password, now login with your new password')

            # logout user and redirect to login page
            logout(request)
            return redirect('signin')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


def Logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index_page')