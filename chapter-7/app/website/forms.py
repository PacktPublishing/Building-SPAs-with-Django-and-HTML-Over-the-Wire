from django import forms
from .models import Comment

class SearchForm(forms.Form):
    search = forms.CharField(
        label="Search",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"id": "search",}
        ),
    )


class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ('name', 'content')