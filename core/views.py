# from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import TemplateView

from acc.views import Login

User = get_user_model()


class Home(Login):
    template_name = "core/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('acc:dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)


class About(TemplateView):
    template_name = "core/about.html"


class Contact(TemplateView):
    template_name = "core/contact.html"
