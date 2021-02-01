import random

def random_text(p=5):
	return ''.join(random.sample(string.ascii_letters+string.digits,p))

def get_usable_name(instance, name=None):
	if not name:
		name=instance.email.split('@')[0]
	exists=instance.__class__.objects.filter(username=name).exists()
	if exists:
		name=instance.email.split('@')[0]
		return get_usable_name(instance, profile, name+random_text())
	return name