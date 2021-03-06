from django.contrib.auth.models import User
from django.db import models
from django.core.validators import URLValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


def user_post_save(sender, instance, **kwargs):
    new_profile = Profile.objects.get_or_create(user=instance)


models.signals.post_save.connect(user_post_save, sender=User)


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(null=True, validators=[URLValidator])
