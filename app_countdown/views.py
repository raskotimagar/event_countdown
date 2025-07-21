from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event
from .forms import EventForm

# Create your views here.
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_countdown', event_id=form.instance.id)
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

def countdown_view(request, event_id):
    event = Event.objects.get(id=event_id)
    current_time = timezone.now()
    time_remaining = event.event_date - current_time

    if time_remaining.total_seconds() < 0:
        time_remaining = 0

    context = {
        'event': event,
        'time_remaining': time_remaining,
        'event_date': event.event_date,
    }
    return render(request, 'countdown.html', context)
