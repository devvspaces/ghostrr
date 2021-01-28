from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, is_active=True, is_staff=False,
                    is_admin=False):
        if not email:
            raise ValueError("User must provide an email")
        if not username:
            raise ValueError("User must provide a username")
        if not password:
            raise ValueError("User must provide a password")

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staff(self, email, username=None, password=None):
        user = self.create_user(email=email, username=username, password=password, is_staff=True)
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(email=email, username=username, password=password, is_staff=True,
                                is_admin=True)
        return user

    def get_staffs(self):
        return self.filter(staff=True)

    def get_admins(self):
        return self.filter(admin=True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username= models.CharField(_('User Name'),max_length=150, unique=True)
    # name = models.CharField(_('Name'),max_length=150)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    # Field for disables accounts
    disabled = models.BooleanField(default=False)

    REQUIRED_FIELDS=['username']
    USERNAME_FIELD = "email"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def get_level(cls):
        return cls.levels[int(cls.level)-1][1]

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'{self.username} : {self.email}'

    def get_absolute_url(self):
        return reverse('login')

    # def email_user(self, subject, message, fail=True):
    #     # print(message)
    #     val = send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[self.email], fail_silently=fail)
    #     return True if val else False

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = 'Ghostrr User'


class Profile(models.Model):
    LEVELS = (
        ('1', 'Free'),
        ('2', 'Pro'),
        ('3', 'Enterprise'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)
    level = models.CharField(max_length=1, choices=LEVELS, default=1)

    def __str__(self):
        return self.user.username




# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         pro=Profile.objects.create(username=username, user=instance)