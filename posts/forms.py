from django import forms

from posts.models import Review


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=('comment',)
