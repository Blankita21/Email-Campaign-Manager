from django.contrib import admin
from .models import Subscriber, Campaign

admin.site.register(Subscriber)
admin.site.register(Campaign)

# from campaigns.models import Subscriber
# subscribers = Subscriber.objects.all()
# subscribers

