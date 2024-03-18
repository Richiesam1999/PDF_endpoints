from django.db import models

# Create your models here.
from django.db import models

class Email(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject