from django.forms import ModelForm
from django.forms.fields import CharField
from django.core.validators import URLValidator
from users.models import Image


class ImageForm(ModelForm):
    url = CharField(validators=[URLValidator])

    class Meta:
        model = Image
        fields = ['user', 'description', 'geolocation', 'url']
