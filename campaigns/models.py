from django.db import models
from django.core.mail import send_mail

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class Campaign(models.Model):
    subject = models.CharField(max_length=100)
    preview_text = models.CharField(max_length=200)
    article_url = models.URLField()
    html_content = models.TextField()
    plain_text_content = models.TextField()
    published_date = models.DateField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    