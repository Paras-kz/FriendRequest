from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' #default username_field was 'username' in default user class
    REQUIRED_FIELDS = ['username'] #'username' field is inherited from AbstractUser
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(CustomUser, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)


