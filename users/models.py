from django.contrib.auth.models import User
from django.db import models
from django.core.validators import URLValidator
from datetime import date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30, blank=True)

    @property
    def age(self):
        days_difference = date.today() - self.date_birth
        return days_difference.days // 365


def user_post_save(sender, instance, **kwargs):
    new_profile = Profile.objects.get_or_create(user=instance)


models.signals.post_save.connect(user_post_save, sender=User)


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    geolocation = models.CharField(max_length=30, blank=True, null=True)
    url = models.URLField(null=True, validators=[URLValidator])
    created_at = models.DateTimeField(auto_now_add=True)
