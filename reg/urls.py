from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views, forms
from .forms import SignUpView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view
         (
             template_name='reg/login.html',
             authentication_form=forms.BootstrapAuthenticationForm
         ),
         name='log_in'),

    path('logout/', LogoutView.as_view(next_page='/'), name='log_out'),
    path('signup/',
         SignUpView.as_view
         (
             extra_context={'title': 'Sign up'}
         ),
         name="signup"),
    path('profile/', views.profile, name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password')
]