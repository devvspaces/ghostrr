import random
import string
import os
import openai
import json

def random_text(p=5):
	return ''.join(random.sample(string.ascii_letters+string.digits,p))

def get_usable_slug(instance, slug=None):
	if not slug:
		slug=random_text()
	exists=instance.__class__.objects.filter(slug=slug).exists()
	if exists:
		return get_usable_slug(instance, slug+random_text())
	return slug



def call_gpt(prompt='', response_length=512):
	api_key = 'sk-d7Ooti8pkq5BsnZrHPDpg5c0ExghIw2pmQbVMwXA'

	openai.api_key = api_key

	response = openai.Completion.create(
		engine="davinci",
		prompt=prompt,
		max_tokens=response_length,
		temperature=0.75,
		# max_tokens=100,
		top_p=1,
		frequency_penalty=0.5,
		presence_penalty=0.5
	)

	return response



# Use json to load simple.config
def get_limit_for_level(level='1'):
	with open('ghostrr/simple_config.json', 'r') as jsfile:
		data = jsfile.read()
	data = json.loads(data)
	try:
		return data[level]
	except KeyError:
		return 0


def write_to_limit(a,b,c):
	limit_dict = dict()
	limit_dict['1'] = int(a)
	limit_dict['2'] = int(b)
	limit_dict['3'] = int(c)
	res = json.dumps(limit_dict)
	with open('ghostrr/simple_config.json', 'w') as jsfile:
		jsfile.write(res)