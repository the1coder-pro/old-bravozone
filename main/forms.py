from django import forms
from .models import PreviousProject
from .models import Comment

class PreviousProjectForm(forms.ModelForm):
    class Meta:
        model = PreviousProject
        fields = ['title', 'content', 'image', 'link', 'date']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
