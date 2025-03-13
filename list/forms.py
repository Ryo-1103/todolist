from django import forms

from .models import TodoItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ["title", "description", "priority"]
        labels = {
            "title": "タイトル",
            "description": "内容",
            "priority": "優先度",
        }
