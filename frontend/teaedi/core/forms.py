from django import forms
from .models import Watcher


class WatcherForm(forms.ModelForm):
    email_id = forms.EmailField()
    events = forms.MultipleChoiceField(choices=Watcher.EVENT_CHOICES)

    class Meta:
        model = Watcher
        fields = ['email_id', 'events']
