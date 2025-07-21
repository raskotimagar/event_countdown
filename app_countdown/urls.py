from django.urls import path
from.import views

urlpatterns= [
    path('', views.create_event_view, name = 'create_event'),
    path('countdown/<str:event_id>/', views.countdown_view, name='event_countdown')
]