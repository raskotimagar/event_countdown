# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('countdown/create/', views.create_event_view, name='create_event'),
    path('countdown/<int:event_id>/', views.countdown_view, name='event_countdown'),
    path('countdown/<int:event_id>/data/', views.countdown_data, name='countdown_data'),
    path('countdown/<int:pk>/update/', views.EventUpdateView.as_view(), name='update_event'),
    path('countdown/<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete_event'),
]