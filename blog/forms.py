from django import forms
from django.conf import settings
from django.shortcuts import get_object_or_404

from accounts.models import User, Profile

from .models import Blogs


class CreateBlogForm(forms.Form):
	title = forms.CharField(max_length=255, help_text='Enter the title you want for this blog here')
	sentence = forms.CharField(widget=forms.TextInput(), help_text='Describe the blog you want to generate here')
	copy_text = forms.CharField(widget=forms.TextInput(), required=False)
	copy_length = forms.IntegerField(help_text='Enter the length of copy you want')

	def save(self, commit=True):
		title = self.cleaned_data.get('title')
		sentence = self.cleaned_data.get('sentence')
		copy_text = self.cleaned_data.get('copy_text')
		copy_length = self.cleaned_data.get('copy_length')

		# Creating new blog
		blog = Blogs(title=title, sentence=sentence, copy_length=copy_length, copy_text=copy_text)
        
		return blog