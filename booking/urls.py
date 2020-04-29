from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('calendar/', views.Calendar.as_view(), name='calendar'),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.Calendar.as_view(), name='calendar'),

    path('book/<int:year>/<int:month>/<int:day>/<int:hour>/<int:min>/<str:bike>/', views.Booking.as_view(), name='book'),
]