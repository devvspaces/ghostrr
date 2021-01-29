from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserRegisterForm
from .models import User, Profile

# Register your models here.
class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	# form = UserUpdateForm
	add_form = UserRegisterForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display=('email', 'username', 'active', )
	list_filter = ('active','staff','admin',)
	search_fields=['email']
	fieldsets = (
		('User', {'fields': ('email', 'username', 'password')}),
		('Permissions', {'fields': ('admin','staff','active',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'password')}
		),
	)
	filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Profile)