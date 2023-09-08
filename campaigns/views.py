from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Subscriber, Campaign
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from .models import Subscriber
from django.contrib.auth.decorators import login_required
from django import forms
from celery import shared_task
from django.contrib import messages


def homepage(request):
    if request.method == 'POST':
        email_to_unsubscribe = request.POST.get('email')  # Get the email from the form
        try:
            subscriber = Subscriber.objects.get(email=email_to_unsubscribe, is_active=True)
            subscriber.is_active = False  # Mark the user as inactive
            subscriber.save()
            messages.success(request, "Unsubscribed successfully.")  # Set a success flash message
        except Subscriber.DoesNotExist:
            messages.error(request, "Email address is not subscribed.")  # Set an error flash message

        return redirect('homepage')  # Redirect back to the homepage

    return render(request, 'home.html')


# def homepage(request):
#     if request.method == 'POST':
#         email_to_unsubscribe = request.POST.get('email')  # Get the email from the form
#         try:
#             subscriber = Subscriber.objects.get(email=email_to_unsubscribe, is_active=True)
#             subscriber.is_active = False  # Mark the user as inactive
#             subscriber.save()
#             return redirect('homepage')  # Redirect back to the homepage
#         except Subscriber.DoesNotExist:
#             error_message = "Email address is not subscribed."
#             context = {'error_message': error_message}
#             return render(request, 'home.html', context)

#     return render(request, 'home.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('send_campaign')  # Redirect to the send_campaign page
        # If authentication fails, or form is not valid, display the login page again
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


# def add_subscriber(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         first_name = request.POST.get('first_name')
#         subscriber = Subscriber(email=email, first_name=first_name)
#         subscriber.save()
#         return JsonResponse({'message': 'Subscriber added successfully.'})
#     return render(request, 'campaigns/add_subscriber.html')


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Subscriber

def add_subscriber(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')

        # Check if the email is already present but inactive
        existing_subscriber = Subscriber.objects.filter(email=email, is_active=False).first()

        if existing_subscriber:
            # If the email is found and inactive, update it to active
            existing_subscriber.is_active = True
            existing_subscriber.save()
            messages.success(request, 'Subscriber reactivated successfully.')
        else:
            # If the email is not found or is active, create a new subscriber
            subscriber = Subscriber(email=email, first_name=first_name)
            subscriber.save()
            messages.success(request, 'Subscriber added successfully.')

        return redirect('add_subscriber')

    return render(request, 'campaigns/add_subscriber.html')



def unsubscribe(request, email):
    subscriber = Subscriber.objects.get(email=email)
    subscriber.is_active = False
    subscriber.save()
    return render(request, 'campaigns/unsubscribe.html')

class CampaignForm(forms.Form):
    subject = forms.CharField(max_length=255)
    preview_text = forms.CharField(max_length=255)
    article_url = forms.URLField()
    html_content = forms.CharField(widget=forms.Textarea)
    plain_text_content = forms.CharField(widget=forms.Textarea)
    published_date = forms.DateField()

@login_required  # Enforce authentication for this view
def send_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            preview_text = form.cleaned_data['preview_text']
            article_url = form.cleaned_data['article_url']
            html_content = form.cleaned_data['html_content']
            plain_text_content = form.cleaned_data['plain_text_content']
            published_date = form.cleaned_data['published_date']

            subscribed_users = Subscriber.objects.filter(is_active=True)

            for user in subscribed_users:
                recipient = user.email
                message = f"Subject: {subject}\n\n"
                message += f"Preview Text: {preview_text}\n\n"
                message += f"Article URL: {article_url}\n\n"
                message += f"HTML Content: {html_content}\n\n"
                message += f"Plain Text Content: {plain_text_content}\n\n"
                message += f"Published Date: {published_date}"

                # send_mail(subject, message, 'paulankitakumari@example.com', [recipient], fail_silently=False)
                send_email_campaign.delay(recipient, subject, message)

            campaign = Campaign.objects.create(
                subject=subject,
                preview_text=preview_text,
                article_url=article_url,
                html_content=html_content,
                plain_text_content=plain_text_content,
                published_date=published_date,
                sent=True  
            )

            return render(request, 'campaigns/send_campaign.html', {'form': form, 'success_message': 'Campaign sent successfully.'})
    else:
        form = CampaignForm()

    return render(request, 'campaigns/send_campaign.html', {'form': form})

@shared_task(bind=True, max_retries=3)  # Adjust max_retries as needed
def send_email_campaign(self, recipient, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='paulankitakumari@example.com',
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")
        # Retry the task with an exponential backoff delay
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
        

