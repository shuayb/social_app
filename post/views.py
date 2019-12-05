from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from rest_framework.exceptions import MethodNotAllowed

from post.forms import PostForm, CommentForm
from post.models import Post
from social_app.common.decorators import ajax_required


class NewPost(LoginRequiredMixin, CreateView):
    template_name = "post/partials/new_post_partial.html"
    form_class = PostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_api_url'] = reverse_lazy("api-post:create")
        return context

    def get(self, *args, **kwargs):
        super().get(self, *args, **kwargs)
        return JsonResponse({'html': render_to_string(self.template_name,
                                                      context=self.get_context_data(),
                                                      request=self.request),
                             'status': 'ok'},
                            safe=False)


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = "post/detail_view.html"
    model = Post


# FBV
@ajax_required
@login_required
def comment_post_modal(request, post_pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm()
        data = {}
        context = {
            'post': post,
            'form': form,
            'user': post.user,
            'comment_api_url': reverse_lazy("api-post:comment",
                                            kwargs={'post_pk': post_pk})
        }

        data['comment_partial_html'] = render_to_string('post/partials/comment_modal_partial.html',
                                                        context=context,
                                                        request=request)
        return JsonResponse(data)
    raise MethodNotAllowed(request.method)
