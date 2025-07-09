from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from .forms import RegistrationForm, EmailAuthenticationForm
from .tokens import emailverificationtoken

from django.utils.decorators import method_decorator
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.decorators import ratelimit

from two_factor.views import LoginView as BasseLoginView
from two_factor.forms import AuthenticationTokenForm, BackupTokenForm

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


# @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
# @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=False), name='dispatch')
class LoginView(BasseLoginView):
    template_name = 'two_factor/core/login.html'
    redirect_authenticated_user = True
    form_list = (
        ('auth', EmailAuthenticationForm),
        ('token', AuthenticationTokenForm),
        ('backup', BackupTokenForm),
    )
   
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Ratelimited:
            return render(request, 'ratelimited.html', status=429)

        if request.method == 'GET' and getattr(request, 'limited', False):
            return render(request, 'ratelimited.html', status=429)

        return response
