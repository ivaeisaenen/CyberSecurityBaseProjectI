from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(verbose_name='message sent', auto_now_add=True)
    def __str__(self):
        return str(self.content) + "," + str(self.user) + "," + str(self.sent_at)