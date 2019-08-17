from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=144)
    subtitle = models.CharField(max_length=144, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '[{}] {}'.format(self.user.username, self.title)

class Calli(models.Model):
    name = models.CharField(max_length=144, blank=True)
    param1 = models.CharField(max_length=144, blank=True)
    param2 = models.CharField(max_length=144, blank=True)
    param3 = models.CharField(max_length=144, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}'.format(self.name)
