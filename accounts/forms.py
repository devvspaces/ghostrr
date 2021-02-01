from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

from social_django.models import UserSocialAuth

from .models import User, Profile



class ResetPasswordValidateEmailForm(forms.Form):
	email=forms.CharField(help_text="Enter your Ghostrr email")

	def clean_email(self):
		email = self.data.get('email')
		validate_email(email)
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist as e:
			raise forms.ValidationError("Email user matched no Ghostrr account")
		
		return email

class UserChangePasswordForm(forms.Form):
	user_pk = forms.IntegerField()
	new_password=forms.CharField(help_text=password_validation.password_validators_help_text_html())
	old_password=forms.CharField(help_text='Enter your old password here')

	# Cleaning password one to check if all validations are met
	def clean_new_password(self):
		ps1=self.cleaned_data.get("new_password")
		password_validation.validate_password(ps1,None)
		return ps1
	
	# This is to check whether the user's old password is correct
	def clean_old_password(self):
		ps1=self.cleaned_data.get("old_password")
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		if not user.check_password(ps1):
			raise forms.ValidationError('Your password is not correct')
		return ps1

	def save(self, commit=True):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		user.set_password(self.cleaned_data.get("new_password"))
		if commit:
			user.save()
		return user



class ForgetPasswordForm(forms.Form):
	user_pk = forms.IntegerField()
	new_password=forms.CharField(help_text=password_validation.password_validators_help_text_html())
	confirm_password=forms.CharField(help_text='Must be similar to first password to pass verification')

	# Cleaning password one to check if all validations are met
	def clean_new_password(self):
		ps1=self.cleaned_data.get("new_password")
		password_validation.validate_password(ps1,None)
		return ps1

	"""Override clean on password2 level to compare similarities of password"""
	def clean_confirm_password(self):
		ps1=self.cleaned_data.get("new_password")
		ps2=self.cleaned_data.get("confirm_password")
		if (ps1 and ps2) and (ps1 != ps2):
			raise forms.ValidationError("The passwords does not match")
		return ps2

	def save(self, commit=True):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		user.set_password(self.cleaned_data.get("new_password"))
		if commit:
			user.save()
		return user


class ChangePasswordForm(forms.Form):
	user_pk = forms.CharField(max_length=255)
	current_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text='Enter your current password here'
	)
	new_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text=password_validation.password_validators_help_text_html()
	)
	confirm_password=forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form__input'}),
		help_text='Must be similar to first password to pass verification'
	)

	# Cleaning old password to check if provided password matches user password
	def clean_current_password(self):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		password = self.cleaned_data.get('current_password')
		if not user.check_password(password):
			raise forms.ValidationError('Your password is not correct')
		return password

	# Cleaning password one to check if all validations are met
	def clean_new_password(self):
		ps1=self.cleaned_data.get("new_password")
		password_validation.validate_password(ps1,None)
		return ps1

	"""Override clean on password2 level to compare similarities of password"""
	def clean_confirm_password(self):
		ps1=self.cleaned_data.get("new_password")
		ps2=self.cleaned_data.get("confirm_password")
		if (ps1 and ps2) and (ps1 != ps2):
			raise forms.ValidationError("The passwords does not match")
		return ps2

	def save(self, commit=True):
		user = get_object_or_404(User, pk=self.cleaned_data.get('user_pk'))
		user.set_password(self.cleaned_data.get("new_password"))
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	email=forms.CharField(widget=forms.EmailInput(), help_text="Enter your email")
	password=forms.CharField(widget=forms.PasswordInput(), help_text="Enter your password")
	def clean(self):
		data=super(LoginForm, self).clean()
		email = data.get('email')
		password = data.get('password')
		validate_email(email)
		try:
			user = User.objects.get(email=email)
			if not user.check_password(password):
				self.add_error('password', forms.ValidationError('Your password is not correct'))
		except User.DoesNotExist as e:
			self.add_error('email', forms.ValidationError("Email user matched no account"))
		return data


class ChangePassword(forms.ModelForm):
	password_old=forms.CharField(label="Old password",widget=forms.PasswordInput)
	password1=forms.CharField(label="New password",widget=forms.PasswordInput)
	password2=forms.CharField(label="Confirm password",widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=("password_old","password1","password2",)
	
	def clean_password2(self):
		#Validating if password1 and 2 are correct
		password1=self.cleaned_data.get("password1")
		password2=self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("New passwords do not match")
		return password2

# class UserUpdateProfile(forms.ModelForm):
# 	class Meta:
# 		model=Profile
# 		fields=("image",'username','id_photo','address','country','state','city',)


class UserRegisterForm(forms.ModelForm):
	password=forms.CharField(label="Password",
							widget=forms.PasswordInput,
							min_length=8,
							help_text=password_validation.password_validators_help_text_html())
	username=forms.CharField(help_text='Enter the username you want to use here', required=False)
	class Meta:
		model=User
		fields=("email","username","password",)
	# Cleaning password one to check if all validations are met
	def clean_password(self):
		ps1=self.cleaned_data.get("password")
		password_validation.validate_password(ps1,None)
		return ps1
	""" Override the default save method to use set_password method to convert text to hashed """
	def save(self, commit=True):
		user=super(UserRegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data.get("password"))
		if commit:
			user.active = True
			
			# # creating profile instance for user
			# if (level > 3) or (level < 1):
			# 	raise form.ValidationError('Invalid level provided')
			
			# try:
			# 	profile = Profile(user=user, level=str(level), credit=settings.CREDITS[level-1])
			# except IndexError:
			# 	profile = Profile(user=user, level=str(level), credit=0)

			user.save()
			# profile.save()


		return user

class UserUpdateForm(forms.ModelForm):
	password=ReadOnlyPasswordHashField()
	class Meta:
		model=User
		fields=("email","username","password","active","staff","admin",)
		def clean_password(self):
			# Regardless of what the user provides, return the initial value.
			# This is done here, rather than on the field, because the
			# field does not have access to the initial value
			return self.initial["password"]

class UserUpdateFormPage(forms.Form):
	email = forms.EmailField(help_text='Enter your email')
	username = forms.CharField(help_text='Enter your username')
	pk = forms.IntegerField()

	def clean_email(self):
		email = self.data.get('email')
		pk = self.data.get('pk')
		validate_email(email)

		# Validate if the email has not been used before
		exists = User.objects.filter(email=email).exclude(pk=pk).exists()
		if exists:
			raise forms.ValidationError('This email has already been used')

		return email
	
	def clean_username(self):
		username = self.data.get('username')
		pk = self.data.get('pk')

		# Validate if the username has not been used before
		exists = User.objects.filter(username=username).exclude(pk=pk).exists()
		if exists:
			raise forms.ValidationError('This username has already been used')

		return username
	
	def save(self, commit=True):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		pk = self.cleaned_data.get('pk')

		# # If this user is a social user, we have to update that
		# UserSocialAuth.objects.get


		user = User.objects.filter(pk=pk).first()

		if user is None:
			# print(pk, '\n\n')
			# # Means this is a social user then get social user instance
			# social_user = get_object_or_404(UserSocialAuth, user_id=pk)

			# print(social_user)
			# print(dir(social_user))
			# print(social_user.user.username)

			# # Create a normal user
			# user = User.objects.create(username=social_user.user.username, email=email)
			pass
		else:
			# Setting new values for normal user
			user.email = email
			user.username = username

		if commit:
			user.save()
		
		return user
		