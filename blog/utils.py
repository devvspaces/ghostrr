import random
import string

def random_text(p=5):
	return ''.join(random.sample(string.ascii_letters+string.digits,p))

def get_usable_slug(instance, slug=None):
	if not slug:
		slug=random_text()
	exists=instance.__class__.objects.filter(slug=slug).exists()
	if exists:
		return get_usable_slug(instance, slug+random_text())
	return slug