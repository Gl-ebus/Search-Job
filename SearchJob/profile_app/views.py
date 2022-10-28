from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from profile_app.forms import RegistrationForm


class RegisterUserView(SuccessMessageMixin, CreateView):
	template_name = 'profile_app/register.html'
	form_class = RegistrationForm
	success_message = 'Вы успешно зарегистрировались,теперь войдите в свой профиль'
	success_url = reverse_lazy('login')


class LoginUserView(SuccessMessageMixin, LoginView):
	# default form_class = AuthenticationForm   (Base class for authenticating users)
	template_name = 'profile_app/login.html'
	success_message = 'Вы успешно вошли'
