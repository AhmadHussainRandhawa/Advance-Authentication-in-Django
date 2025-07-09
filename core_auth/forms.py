from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.contrib.auth.forms import UsernameField
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_variables

UserModel = get_user_model()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False  # Will activate after email click
        if commit:
            user.save()
        return user
    

class EmailAuthenticationForm(forms.Form):
    """
    Authentication form that works with a custom user model using email as USERNAME_FIELD.
    Compatible with AbstractUser or AbstractBaseUser+PermissionsMixin.
    """

    email = UsernameField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password. Note that both fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Introspect model to get correct label/max_length
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        self.fields["email"].label = capfirst(self.email_field.verbose_name)
        self.fields["email"].max_length = self.email_field.max_length
        self.fields["email"].widget.attrs["maxlength"] = self.email_field.max_length

    @method_decorator(sensitive_variables("password"))
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(self.error_messages["inactive"], code="inactive")

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email_field.verbose_name},
        )
