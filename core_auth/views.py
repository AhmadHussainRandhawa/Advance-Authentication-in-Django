from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from .forms import RegistrationForm
from .tokens import emailverificationtoken

User = get_user_model()

class RegisterView(View):
    
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/register/register.html', {'form':form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            self.send_activation_email(request, user)
            return render(request, 'registration/register/register_pending.html')
        return render(request, 'registration/register/register.html', {'form': form})

    def send_activation_email(self, request, user):        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = emailverificationtoken.make_token(user)
        activation_link = request.build_absolute_uri(
            reverse('core_auth:activate', kwargs={'uidb64': uid, 'token': token}))

        context = {'user':user, 'activation_link':activation_link}

        subject = "Activate your AuthForge Account"
        message = render_to_string('registration/register/activation_email.html', context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(User.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None 

        if user and emailverificationtoken.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'registration/register/activation_success.html')
        
        else: 
            return render(request, 'registration/register/activation_invalid.html')
