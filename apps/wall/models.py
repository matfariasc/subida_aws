from django.db import models
from apps.users.models import Users

# Create your models here.
class messages(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users,related_name="all_messages", on_delete=models.CASCADE)
    user_message = models.ForeignKey(Users,related_name="message_user", on_delete=models.CASCADE)

class comments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(messages,related_name="all_comments", on_delete=models.CASCADE)
    user = models.ForeignKey(Users,related_name="all_users", on_delete=models.CASCADE)
