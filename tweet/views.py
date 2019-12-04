from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from rest_framework.exceptions import MethodNotAllowed

from social_app.common.decorators import ajax_required
from tweet.forms import TweetForm
from tweet.models import Tweet


# @method_decorator(ajax_required, name='dispatch')
# class NewTweet(CreateView):
#     template_name = "tweet/new_tweet.html"
#     form_class = TweetForm
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['create_url'] = reverse_lazy("api-tweet:create")
#         return context


class NewTweet(LoginRequiredMixin, CreateView):
    template_name = "tweet/partials/new_tweet_post_partial.html"
    form_class = TweetForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_api_url'] = reverse_lazy("api-tweet:create")
        return context

    def get(self, *args, **kwargs):
        super().get(self, *args, **kwargs)
        return JsonResponse({'html': render_to_string(self.template_name,
                                                      context=self.get_context_data(),
                                                      request=self.request),
                             'status': 'ok'},
                            safe=False)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweet/detail_view.html"
    model = Tweet


# FBV
@ajax_required
@login_required
def reply_tweet_modal(request, tweet_pk):
    if request.method == 'GET':
        tweet = get_object_or_404(Tweet, pk=tweet_pk)
        tweet_form = TweetForm()
        data = {}
        context = {
            'tweet': tweet,
            'form': tweet_form,
            'user': tweet.user,
            'reply_api_url': reverse_lazy("api-tweet:reply",
                                          kwargs={'tweet_pk': tweet_pk})
        }

        data['reply_partial_html'] = render_to_string('tweet/partials/reply_modal_partial.html',
                                                      context=context,
                                                      request=request)
        return JsonResponse(data)
    raise MethodNotAllowed(request.method)
