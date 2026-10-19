from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "pinned"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title", "autofocus": True}),
            "content": forms.Textarea(attrs={"placeholder": "Write your note...", "rows": 12}),
        }
