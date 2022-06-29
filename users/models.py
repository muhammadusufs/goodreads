from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    profile_pic = models.ImageField(default='profile_img.jpg')
    friends = models.ManyToManyField("CustomUser", blank=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name='from_user', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name='to_user', on_delete=models.CASCADE
    )
