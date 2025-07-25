from django import forms
from .models import Event
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'description']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-input w-full px-4 py-3 rounded-lg bg-white text-black dark:bg-gray-800 dark:text-white appearance-auto focus:outline-none focus:ring-2 focus:ring-primary'
            },
            format='%Y-%m-%dT%H:%M'
            )
        }
    
    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date <= timezone.now():
            raise forms.ValidationError("Event date must be in the future")
        return event_date