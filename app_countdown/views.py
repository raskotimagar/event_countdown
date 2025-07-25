# views.py - Enhanced functionality
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .models import Event
from .forms import EventForm

def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_countdown', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def countdown_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
        'event_date_iso': event.event_date.isoformat(),
    }
    return render(request, 'countdown.html', context)

def countdown_data(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    now = timezone.now()
    time_remaining = event.event_date - now
    seconds_remaining = max(time_remaining.total_seconds(), 0)
    
    return JsonResponse({
        'name': event.name,
        'total_seconds': seconds_remaining,
        'expired': event.status() == "expired",
        'event_date': event.event_date.isoformat(),
    })

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    ordering = ['event_date']
    
    def get_queryset(self):
        # Return upcomin events sorted by closest first
        return Event.objects.filter(
            event_date__gte=timezone.now()
        ).order_by('event_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now= timezone.now()

        # Get event statistics
        total_events = Event.objects.count()
        upcoming_count = Event.objects.filter(event_date__gte = now).count()
        completed_count =total_events - upcoming_count

        # Add statistics to context
        context.update({
            'total_events':total_events,
            'upcoming_count':upcoming_count,
            'completed_count': completed_count,
            'now':now,
        })
        return context

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')
    
    def form_valid(self, form):
        if form.instance.event_date <= timezone.now():
            form.add_error('event_date', "Event date must be in the future")
            return self.form_invalid(form)
        return super().form_valid(form)

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list')