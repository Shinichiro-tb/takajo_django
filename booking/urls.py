from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('calendar/', views.Calendar.as_view(), name='calendar'), #予約カレンダーのURL
    path('calendar/<int:year>/<int:month>/<int:day>/', views.Calendar.as_view(), name='calendar'), #予約カレンダーのURLの時間指定バージョン

    path('book/<int:year>/<int:month>/<int:day>/<int:hour>/<int:min>/<str:bike>/', views.Booking.as_view(), name='book'), #予約詳細の画面へのURL

    path('mypage/<int:year>/<int:month>/<int:day>/<int:hour>/<int:min>/<str:bike>/', views.Mypage.as_view(), name='mypage'), #マイページ(貸出・削除・返却ページ)
    
    path('use/<int:year>/<int:month>/<int:day>/<int:hour>/<int:min>/<str:bike>/', views.Use.as_view(), name='use'), #使用開始ページ

    path('delete/<int:pk>/', views.BookingDelete.as_view(), name='booking_delete'),
]