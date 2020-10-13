import datetime
from django.db.models import Q #データベース検索に使うhttps://qiita.com/okoppe8/items/66a8747cf179a538355b ⇐ここ見て（クエリの文法）！
from django.views import generic
from booking.models import Biketype, Schedule

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from booking.forms import BookForm

#from django.http import HttpResponse
#from django.shortcuts import render
#from django.utils import timezone

#print(type(difference_day)) #型確認
#print("\n")


###予約一覧カレンダー
class Calendar(generic.TemplateView):
    """
    予約一覧カレンダービュー
    """
    template_name = 'booking/calendar.html'

    def get_context_data(self, **kwargs):
        """htmlに値を送るための準備"""
        context = super().get_context_data(**kwargs)

        ##自転車をリストに格納
        bikelist = []
        for A in Biketype.objects.all():
            #print(A)
            bikelist.append(A.bikename)

        ##今日の日付の取得
        today = datetime.date.today() 

        ##どの日を基準にカレンダーを表示するかの処理
        #URLから取得
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        #年月日の指定があれば
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        #なければ今日(基本はこっち)
        else:
            base_date = today  #date型

        ##曜日取得
        day_list = ["月","火","水","木","金","土","日"]
        day_of_the_week = day_list[base_date.weekday()]


        ###8:00〜22:00までのカレンダーを作成する
        ##時間のリストを作る
        dt = datetime.datetime(2020, 4, 1, 8, 0, 0) #2020/4/1は全く必要ない（時刻計算上,型が違うと大変なんです）https://qiita.com/tekitoh/items/00f5afe0faadb27846b0
        time = dt.time() #time型

        timelist = [] #時間の刻みのリスト
        e_time = datetime.time(22, 00, 00) #貸出終了時間

        while (time < e_time):
            timelist.append(time)
            dt = dt + datetime.timedelta(minutes=15) #15分の刻み
            time = dt.time()

        calendar = {} #空の辞書(カレンダー)を用意する
        for time in timelist:
            row = {}
            for bike in bikelist:
                row[bike] = True
            calendar[time] = row

        ###予約の取得

        start_time = datetime.time(8, 00, 00) #予約可能開始時間
        end_time = datetime.time(22,00, 00) #予約可能終了時間
        message = ""

        ### コメントアウト中の()のなかは構文や変数
        ### Scheduleクラスから 予約されたdateがいま表示されているカレンダーの日付と一緒(filter)のであるところの
        ##  ①貸出開始時間(start)が貸出期限(end_time(22:00))を超える(__gt) 
        #                           または
        ##  ②貸出終了時間(end)が貸出はじめ(start_time(8:00))未満(__lt)            ではない(exclude)所をscheduleに引き渡す

        for schedule in Schedule.objects.filter(date=base_date).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):

            book_start_time = schedule.start #time型 予約の開始時刻を取得
            book_end_time = schedule.end #time型 予約の終了時刻を取得
            user_name = schedule.user  #使用者の名前

            #print(type(schedule.biketype))
            bike_type = str(schedule.biketype) #自転車の種類を取得

            #予約データ確認
            if book_start_time in calendar and bike_type in calendar[book_start_time]:
                calendar[book_start_time][bike_type] = user_name

                while (book_start_time < book_end_time):
                    cast_start_time = datetime.datetime.combine(base_date, book_start_time) + datetime.timedelta(minutes=15) #datetime型
                    book_start_time = cast_start_time.time() #time型
                    if (calendar[book_start_time][bike_type] == True):
                        calendar[book_start_time][bike_type] = False
                        #message = "予約完了"
                    else:
                        message = "予約ができてない可能性があります。確認を！！"
                        #messages.error(self.request, 'ブッキング！！！')
                        #return redirect('booking:book', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

        ## htmlに値を渡す
        context['date'] = base_date
        context['day'] = day_of_the_week
        context['before'] = base_date - datetime.timedelta(days=1)
        context['after'] = base_date + datetime.timedelta(days=1)
        context['bikelist'] = bikelist
        context['calendar'] = calendar
        context['message'] = message

        return context


class Booking(generic.CreateView):
    """
    予約フォームを作る
    https://qiita.com/felyce/items/7d0187485cad4418c073 参考
    """
    model = Schedule
    form_class = BookForm
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        """htmlに値を送るための準備"""
        context = super().get_context_data(**kwargs) #URLから情報を取得
        return context

    def form_valid(self, form):
        """バリデーションを通った時"""
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('min')
        bike = self.kwargs.get('bike') #どの自転車を使うか
        bike_name = get_object_or_404(Biketype, bikename=bike)

        date = datetime.date(year=year, month=month, day=day) #date型 予約日
        start = datetime.time(hour=hour, minute=minute) #time 予約開始時間

        end_str = self.request.POST.get('end') #str型 form入力データ

        ##計算のために型を変換する
        start_dt = datetime.datetime.combine(date, start) #datetime 予約日+予約開始
        
        date_str = date.strftime("%Y/%m/%d") #予約日を文字列型に
        dt_str = date_str + end_str #予約日+終了時間（文字列の足し算）
        end_dt = datetime.datetime.strptime(dt_str, "%Y/%m/%d%H:%M:%S") #datetime型に変換

        ##時間計算
        difference = end_dt - start_dt #使用時間 timedelta
        difference_sec = difference.seconds #時間部分を秒に直す int
        difference_day = difference.days * 86400 #日付差分を秒に治す int
        difference_all = difference_sec + difference_day

        if (difference_all > 10800):
            messages.error(self.request, '3時間超えてますよ〜')
            return redirect('booking:book', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

        elif(difference_all <= 0):
            messages.error(self.request, "開始時間より終了時間のほうがまえになってますよ〜")
            return redirect('booking:book', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

        else:
            schedule = form.save(commit=False)
            schedule.date = date
            schedule.start = start
            schedule.biketype = bike_name
            schedule.save()
            return redirect('booking:calendar')

    def form_invalid(self, form):
        """バリデーションを通らなかったとき"""
        messages.warning(self.request, 'もう一度入力してね')
        return super().form_invalid(form)


class Mypage(generic.TemplateView):
    """
    予約の個人ページ
    """
    template_name = 'booking/my_page.html'

    def get_context_data(self, **kwargs):
        """htmlにデータを送る準備(個人ページの)"""
        context = super().get_context_data(**kwargs)
        
        #URLから取得
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        booking_date = datetime.date(year=year, month=month, day=day) #貸出予定の日にち

        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('min')
        booking_s_time = datetime.time(hour, minute) #貸出開始予定時間

        bike = str(self.kwargs.get('bike'))
        #print(bike)

        #自転車と自転車のidをリストに格納
        bikelist = []
        for A in Biketype.objects.all():
            b_list = [A.id, A.bikename]
            bikelist.append(b_list)
        print(bikelist)

        number=0 #カウント変数
        #bike_idの検索
        while (bikelist[number][1] != bike):
            number += 1
        bike_id = bikelist[number][0] #予約された自転車のid
        print(bike_id)


        #scheduleからmypageに表示するユーザーを探し当てる
        for schedule in Schedule.objects.filter(date=booking_date, start=booking_s_time, biketype=bike_id):
            booking_e_time = schedule.end
            user_name = schedule.user

        print(booking_e_time)
        print(user_name)

        context['date'] = booking_date
        context['s_time'] = booking_s_time
        context['e_time'] = booking_e_time
        context['ueser'] = user_name
        context['bike'] = bike

        return context