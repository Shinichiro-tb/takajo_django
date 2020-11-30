"""管理サイト(http://127.0.0.1:8000/admin/)へ表示したいモデルを追加する"""

from django.contrib import admin
from booking.models import Biketype, Schedule, Lending_book

class BiketypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bikename',) #一覧に出す項目
    list_display_links = ('id', 'bikename',) #修正リンクの項目

admin.site.register(Biketype, BiketypeAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    """
    予約簿
    """
    list_display = ('id', 'date', 'start', 'end', 'user', 'biketype',)
    list_display_links = ('id', 'user',)
    #raw_id_fields = ('biketype',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防)

admin.site.register(Schedule, ScheduleAdmin)

class Lending_bookAdmin(admin.ModelAdmin):
    """
    貸出簿
    """
    list_display = ('id', 'booking_id', 'l_date', 'l_start', 'l_end', 'l_user', 'l_biketype', 'l_place',)
    list_display_links = ('id', 'l_user',)

admin.site.register(Lending_book, Lending_bookAdmin)

