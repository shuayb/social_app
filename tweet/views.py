from django.urls import reverse_lazy
from django.views.generic import CreateView

from tweet.forms import TweetForm


class NewTweet(CreateView):
    template_name = "tweet/new_tweet.html"
    form_class = TweetForm

    def get_context_data(self, *args, **kwargs):
        context = super(NewTweet, self).get_context_data(*args, **kwargs)
        context['create_url'] = reverse_lazy("api-tweet:create")
        return context
