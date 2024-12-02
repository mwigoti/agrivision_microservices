from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from .forms import CustomUserCreationForm, CustomPasswordResetForm
from .models import CustomUser

from django.shortcuts import render

def base (request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send verification email
            subject = 'Verify your email address'
            html_message = render_to_string('registration/verification_email.html', {
                'user': user,
                'token': user.verification_token,
                'domain': request.get_host(),
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=html_message,
            )
            
            messages.success(request, 'Please check your email to verify your account.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_email_verified = True
        user.verification_token = ''
        user.save()
        messages.success(request, 'Your email has been verified. You can now login.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')
