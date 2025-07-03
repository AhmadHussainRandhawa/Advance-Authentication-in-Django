from django.urls import reverse_lazy
from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, logout_then_login,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
    )

app_name = 'core_auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password-change/', PasswordChangeView.as_view(
        success_url=reverse_lazy('core_auth:password_change_done')), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(
        success_url=reverse_lazy('core_auth:password_reset_done')), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('core_auth:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
