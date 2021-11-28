from django.db import models
from accounts.models import User


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='media')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')

    class Meta:
        ordering = ['created_at']
