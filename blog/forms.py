import string

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
	copy_length = forms.IntegerField(help_text='Select the length of copy you want')

	def clean_copy_length(self):
		copy_length = int(self.data.get('copy_length'))

		if copy_length not in [1,2]:
			raise forms.ValidationError('Invalid length selected')
		return copy_length
	
	def clean_title(self):
		title = self.data.get('title')

		if len(title.split(' ')) < 4:
			raise forms.ValidationError('Title is too short')
		return title

	def clean_sentence(self):
		sentence = self.data.get('sentence')

		sentence_split = sentence.split('.')
		sentence_len = len(sentence_split)

		# Validate length
		if sentence_len < 4:
			raise forms.ValidationError('Input sentences are too few')

		# Validate words length
		word_len = 0
		for i in sentence_split:
			word_len += len(i.split(' '))
		
		if word_len < 50:
			raise forms.ValidationError('Input sentences are too short, Consider making the sentences longer or add another sentence.')
		
		# Validate length extra
		word_avg = word_len / sentence_len
		if word_avg < 15:
			raise forms.ValidationError('Sentences entered are too short, Consider making the sentences more longer or meaningful.')
		
		# Reducing punctuation marks
		for i in string.punctuation:
			sentence = sentence.replace(i+i,i)

		return sentence

	def save(self, commit=True):
		title = self.cleaned_data.get('title')
		sentence = self.cleaned_data.get('sentence')
		copy_text = self.cleaned_data.get('copy_text')
		copy_length = self.cleaned_data.get('copy_length')

		# Creating new blog
		blog = Blogs(title=title, sentence=sentence, copy_length=copy_length, copy_text=copy_text)
        
		return blog