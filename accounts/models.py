from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
DEFAULT = 'default.png'

class User(AbstractUser):

    avatar = models.ImageField(upload_to = 'accounts', default='default.png')

    def __str__(self):
        return "@{}".format(self.username)

    def set_image_to_default(self):
        self.avatar.delete(save=False)  # delete old image file
        self.avatar = DEFAULT
        self.save()
