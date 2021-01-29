from django import forms
from django.conf import settings
from django.shortcuts import get_object_or_404

from accounts.models import User, Profile

from .models import Blogs
from .utils import get_limit_for_level, write_to_limit



class EditLimitForm(forms.Form):
	free_limit = forms.IntegerField(help_text='Enter the limit for the free users')
	pro_limit = forms.IntegerField(help_text='Enter the limit for the pro users')
	enterprise_limit = forms.IntegerField(help_text='Enter the limit for the enterprise users')

	def save(self):
		free_limit = self.cleaned_data.get("free_limit")
		pro_limit = self.cleaned_data.get("pro_limit")
		enterprise_limit = self.cleaned_data.get("enterprise_limit")
		write_to_limit(free_limit, pro_limit, enterprise_limit)
		return 'Saved'


class CreateBlogForm(forms.Form):
	pk = forms.IntegerField()
	title = forms.CharField(max_length=255, help_text='Enter the title you want for this blog here')
	sentence = forms.CharField(widget=forms.TextInput(), help_text='Describe the blog you want to generate here')
	copy_text = forms.CharField(widget=forms.TextInput(), required=False)
	copy_length = forms.IntegerField(help_text='Enter the length of copy you want')

	def clean_copy_length(self):
		pk = self.data.get('pk')
		# Get user form pk
		user = get_object_or_404(User, pk=pk)
		print('hohoho here\n\n')

		copy_length = int(self.data.get('copy_length'))
		limit = int(get_limit_for_level(user.profile.level))
		
		if (copy_length > limit) and (limit != -1):
			raise forms.ValidationError(f"You have passed your copy limit of {limit}, if you want more copy length upgrade to pro.")
		
		return copy_length

	def save(self, commit=True):
		title = self.cleaned_data.get('title')
		sentence = self.cleaned_data.get('sentence')
		copy_text = self.cleaned_data.get('copy_text')
		copy_length = self.cleaned_data.get('copy_length')

		# Creating new blog
		blog = Blogs(title=title, sentence=sentence, copy_length=copy_length, copy_text=copy_text)
        
		return blog