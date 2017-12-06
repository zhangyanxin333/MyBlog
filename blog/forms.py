from .models import Comment
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        ####通过模型创建表单
        model = Comment
        fields =('name','body')


