from django.urls import path

from .views import (
    LogInView, SignUpView, ActivateView, LogOutView, LogOutConfirmView,
    ResendActivationCodeView,
)

from django.views.generic import TemplateView
'''
     RemindUsernameView, 
    ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView,
'''



app_name = 'account_test'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/confirm/', LogOutConfirmView.as_view(), name='log_out_confirm'),
    path('log-out/', LogOutView.as_view(), name='log_out'),

   

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),
]
