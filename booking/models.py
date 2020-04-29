"""
### 自転車貸出
### データベースに記録したいデータを定義する
"""
### ここを編集したら ###
## models.pyの変更を拾ってマイグレートファイルを作る
# python manage.py makemigrations booking

## マイグレートファイルをデータベースに反映する
# python manage.py migrate

## この2つのコマンドを打つ！！


from django.db import models
import datetime

class Biketype(models.Model):
    """自転車の種類"""
    bikename = models.CharField('自転車の種類', max_length=255)

    def __str__(self):
        return self.bikename

class Schedule(models.Model):
    """予約スケジュール"""
    date = models.DateField('利用日')
    start = models.TimeField('開始時間')
    end = models.TimeField('終了時間')
    user = models.CharField('名前', max_length=255)
    biketype = models.ForeignKey(Biketype, verbose_name='使用自転車', on_delete=models.CASCADE) #自転車の種類と紐付け

    def __str__(self):
        start = self.start.strftime('%H:%M:%S') #date型を'文字列型'に変換
        end = self.end.strftime('%H:%M:%S')
        date = self.date.strftime('%Y/%m/%d')
        return f'{self.user} {start} ^ {end} {date} {self.biketype}'
