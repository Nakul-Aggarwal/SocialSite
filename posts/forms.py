from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "group", "picture")
        model = models.Post

    widgets = {
        "message": forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
    }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = (
                models.Group.objects.filter(
                    pk__in=user.groups.values_list("group__pk")
                )
            )


class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ('text','picture')

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
