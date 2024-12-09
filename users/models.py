from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.png', upload_to='profile_pics')



    def __str__(self):
        return f'{self.user.username} Profile'


    
    def save(self, *args, **kwargs):
        super().save()

        imgs = Image.open(self.img.path)

        if imgs.height > 300 or imgs.width > 300:
            output_size = (300, 300)
            imgs.thumbnail(output_size)
            imgs.save(self.img.path)