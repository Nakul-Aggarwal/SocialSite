from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# pip install django-braces
from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__exact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group','picture')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

class DeleteComment(LoginRequiredMixin, generic.DeleteView):
    model = models.Comment
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Comment Deleted")
        return super().delete(*args, **kwargs)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == "POST":
        form = forms.CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:single', username=post.user.username, pk=post.pk)
    else:
        form = forms.CommentForm()
    return render(request, 'posts/comment_form.html', {'form': form, 'post':post})
