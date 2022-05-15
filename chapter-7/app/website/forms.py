from django import forms
from .models import Comment


class SearchForm(forms.Form):
    search = forms.CharField(
        label="Search",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "search",
                "class": "input",
                "placeholder": "Title...",
            }
        ),
    )


class CommentForm(forms.ModelForm):

    author = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "author",
                "class": "input",
                "placeholder": "Your name...",
            }
        ),
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "content",
                "class": "input",
                "placeholder": "Your comment...",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ("author", "content", "post")
