from django import forms
from .models import BlogPost, Tag
from django.forms.widgets import ClearableFileInput


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'image', 'public', 'tags']
        labels = {'title': '', 'text': ''}
        widgets = {'title': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
                   'text': forms.Textarea(attrs={'cols': 80})}


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        labels = {'title': ''}
        widgets = {'title': forms.Textarea(attrs={'cols': 80, 'rows': 1})}
