"""管理サイト(http://127.0.0.1:8000/admin/)へ表示したいモデルを追加する"""

from django.contrib import admin
from booking.models import Biketype, Schedule

class BiketypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bikename',) #一覧に出す項目
    list_display_links = ('id', 'bikename',) #修正リンクの項目

admin.site.register(Biketype, BiketypeAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'start', 'end', 'user', 'biketype',)
    list_display_links = ('id', 'user',)
    #raw_id_fields = ('biketype',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防)

admin.site.register(Schedule, ScheduleAdmin)