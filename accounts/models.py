from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    photo = models.ImageField('Фотография', upload_to='users/profile/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)