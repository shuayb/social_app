# from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView

from acc.forms import UserRegistrationForm, UserAuthenticationForm, UpdateUserProfileForm
from tweet.forms import TweetForm

User = get_user_model()


class ToProfile(LoginRequiredMixin, View):
    # Todo: Improve this, could use generic.base RedirectView
    def get(self, request, *args, **kwargs):
        return redirect('core:user-profile', request.user.username)


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "acc/dashboard.html"
    # Using ajax instead of this way, keeping dashboard as light as possible.
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['create_form'] = TweetForm()
    #     context['create_url'] = reverse_lazy("api-tweet:create")
    #     return context


class Login(LoginView):
    template_name = "acc/login.html"
    form_class = UserAuthenticationForm

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


class Logout(LoginRequiredMixin, LogoutView):
    template_name = "acc/logout.html"


# Todo: Use form view, override save() method of model
# Todo Test cookies, if user has them enabled
class Register(View):
    form_class = UserRegistrationForm
    template_name = "acc/register.html"

    @method_decorator(sensitive_post_parameters('password', 'password2'))
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # request.session.set_test_cookie()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = new_user.username.lower()
            new_user.email = new_user.email.lower()
            new_user.is_active = True
            new_user.email_confirmed = False
            new_user.save()

            # Todo send mail
            # mail = "it is todo"
            # messages.success(request, 'A verification email has been sent to ' + str(mail) + "!")

            new_user = authenticate(email=new_user.email,password=form.cleaned_data.get('password'))
            login(request, new_user)
            return redirect('acc:dashboard')

        return render(request, self.template_name, {'form': form})


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserProfileForm
    template_name = "acc/update_profile.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self, *args, **kwargs):
        username = User.objects.get(id=self.request.user.id).username
        return reverse('core:user-profile', args=[username])


class Profile(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    template_name = 'acc/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if self.request.user.username != self.kwargs.get('slug'):
            context['is_following'] = User.objects.is_following(self.request.user,
                                                                User.objects.get(username=slug))
        else:
            context['is_following'] = None
        return context
