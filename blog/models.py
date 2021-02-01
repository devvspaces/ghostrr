from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import get_usable_slug

# Create your models here.
class Blogs(models.Model):
    LENGTHS = (
        ('1', 'Minimum Word 500',),
        ('2', 'Maximum Word 1000',),
    )
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    sentence = models.CharField(max_length=500)
    copy_length = models.CharField(choices=LENGTHS, max_length=1)
    copy_text = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return f'{self.profile.user.username}: Blog {self.title}'


@receiver(post_save, sender=Blogs)
def create_blog(sender, instance, created, **kwargs):
    if created:
        slug = get_usable_slug(instance)
        instance.slug = slug
        instance.save()