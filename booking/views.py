import datetime
from django.db.models import Q #データベース検索に使うhttps://qiita.com/okoppe8/items/66a8747cf179a538355b ⇐ここ見て（クエリの文法）！
from django.views import generic
from booking.models import Biketype, Schedule, Lending_book #参考までにhttps://btj0.com/blog/django/method-attribute/

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from booking.forms import BookForm, LendingForm
from django.urls import reverse_lazy, reverse

#from django.http import HttpResponse
#from django.shortcuts import render
#from django.utils import timezone

def user_surch(bike_id, booking_date, booking_s_time):
    """予約表のデータベースからユーザーを探す（バイクの種類, 予約日, 予約開始時刻）[0]⇛終わりの時間、[1]⇛ユーザー、[2]⇛id"""
    #scheduleからmypageに表示するユーザーを探し当てる
    for schedule in Schedule.objects.filter(date=booking_date, start=booking_s_time, biketype=bike_id):
        booking_e_time = schedule.end
        user_name = schedule.user
        booking_id = schedule.id
    #print(booking_e_time)
    #print(user_name)
    return booking_e_time, user_name, booking_id

def distplay_time(hour, minute):
    """時間表示をきれいにする(時, 分)"""
    if(hour<10):
        hour_str = "0" + str(hour)
    else:
        hour_str = hour
    if(minute<10):
        minute_str = "0" + str(minute)
    else:
        minute_str =minute

    return hour_str, minute_str

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
                cast_start_time = datetime.datetime.combine(base_date, book_start_time) + datetime.timedelta(minutes=15) #datetime型、予約開始時間に15分足す
                book_start_time = cast_start_time.time() #time型、時間だけ取り出す

                while (book_start_time < book_end_time):
                    if (calendar[book_start_time][bike_type] == True):
                        calendar[book_start_time][bike_type] = False
                        cast_start_time = datetime.datetime.combine(base_date, book_start_time) + datetime.timedelta(minutes=15) #datetime型
                        book_start_time = cast_start_time.time() #time型
                        #message = "予約完了"
                    else:
                        message = "予約ができてない可能性があります。確認を！！"
                        cast_start_time = datetime.datetime.combine(base_date, book_start_time) + datetime.timedelta(minutes=15) #datetime型
                        book_start_time = cast_start_time.time() #time型

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

        context['hour'] = distplay_time(self.kwargs.get('hour'), self.kwargs.get('min'))[0]
        context['minute'] = distplay_time(self.kwargs.get('hour'), self.kwargs.get('min'))[1]
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

        booking_date = datetime.date(year=year, month=month, day=day) #date型 予約日
        booking_s_time = datetime.time(hour=hour, minute=minute) #time 予約開始時刻

        end_str = self.request.POST.get('end') #str型 form入力データ
        #print(end_str)
        if (end_str==""): #終了時間を入力しなかったら
            messages.error(self.request, '予約終了時間書いてください')
            return redirect('booking:book', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)
        if (len(end_str)<=5): #秒まで入力しなかったら
            end_str += ":00" 
        #print(end_str)

        ##計算のために型を変換する
        start_dt = datetime.datetime.combine(booking_date, booking_s_time) #datetime 予約日+予約開始
        
        date_str = booking_date.strftime("%Y/%m/%d") #予約日を文字列型に
        dt_str = date_str + end_str #予約日+終了時間（文字列の足し算）
        end_dt = datetime.datetime.strptime(dt_str, "%Y/%m/%d%H:%M:%S") #datetime型に変換 予約終了日時

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
            #schedule（データベース・予約表）から同じ自転車をその日に予約したユーザーを探し当てる
            for schedule_list in Schedule.objects.filter(date=booking_date, biketype=bike_name):
                #booking_list_number = schedule_list.id
                booking_list_s_time = schedule_list.start #予約表の"あるユーザ"の予約開始時刻
                booking_list_e_time = schedule_list.end #予約表の"あるユーザ"の予約終了時刻
                #user_list_name = schedule_list.user
                print(booking_list_s_time) #
                print(end_dt.time()) #いま入力した人の予約終了時刻
                print("\n")
                if (booking_list_s_time < end_dt.time() and end_dt.time() < booking_list_e_time):
                    messages.error(self.request, '終了時間が他の利用者とかぶっています')
                    return redirect('booking:book', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

                elif (start_dt.time() < booking_list_s_time and booking_list_e_time < end_dt.time()):
                    messages.error(self.request, '予約時間が他の利用者とかぶっています')
                    return redirect('booking:book', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

            schedule = form.save(commit=False)
            schedule.date = booking_date
            schedule.start = booking_s_time
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
        bike_name = get_object_or_404(Biketype, bikename=bike)
        #print(bike)

        context['hour'] = distplay_time(hour, minute)[0]
        context['minute'] = distplay_time(hour, minute)[1]
        context['e_time'] = user_surch(bike_name, booking_date, booking_s_time)[0]
        context['user'] = user_surch(bike_name, booking_date, booking_s_time)[1]
        context['booking_id'] = user_surch(bike_name, booking_date, booking_s_time)[2]
        return context

class Use(generic.CreateView):
    """
    利用開始ページ
    """
    model = Lending_book
    form_class = LendingForm
    template_name = 'booking/use.html'

    def get_context_data(self, **kwargs):
        """htmlにデータを送る準備"""
        context = super().get_context_data(**kwargs) #URLから情報を取得
        context['hour'] = distplay_time(self.kwargs.get('hour'), self.kwargs.get('min'))[0]
        context['minute'] = distplay_time(self.kwargs.get('hour'), self.kwargs.get('min'))[1]
        return context

    def form_valid(self, form):
        """バリデーションを通った時"""
        #貸出開始日付・時刻を取得
        l_dt = datetime.datetime.now()
        l_date = l_dt.date()
        l_s_time = l_dt.time()

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        minute = self.kwargs.get('min')

        booking_date = datetime.date(year=year, month=month, day=day) #date型 予約日
        booking_s_time = datetime.time(hour=hour, minute=minute) #time 予約開始時間
        booking_datetime = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute) #datetime

        bike = self.kwargs.get('bike') #どの自転車を使うか
        bike_name = get_object_or_404(Biketype, bikename=bike)

        #予約日と開始日の一致の確認
        if (l_date != booking_date):
            messages.error(self.request, "予約した日に借りましょ！")
            return redirect('booking:use', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

        else:
            if (l_dt < booking_datetime): #現在時刻が予約時刻より前だったら
                l_difference = l_dt - booking_datetime #予約開始時間と現在時刻の差 timedelta
                l_difference_sec = l_difference.seconds #時間部分を秒に直す int
                #print(l_difference_sec)
                #予約時間時間
                if (l_difference_sec > 600): #10分（600秒）以上だったら
                    messages.error(self.request, "予約開始の10分前から借りられます！")
                    return redirect('booking:use', year=year, month=month, day=day, hour=hour, min=minute, bike=bike)

            else:
                use_start = form.save(commit=False)
                use_start.booking_id = self.kwargs.get('booking_id')
                use_start.l_date = l_date
                use_start.l_user = user_surch(bike_name, booking_date, booking_s_time)[1]
                use_start.l_start = l_s_time
                use_start.l_end = l_s_time
                use_start.l_biketype = bike_name
                use_start.save()
                return redirect('booking:calendar')

    def form_invalid(self, form):
        """バリデーションを通らなかったとき"""
        messages.warning(self.request, 'もう一度入力してね')
        return super().form_invalid(form)

class BookingDelete(generic.DeleteView):
    """
    予約削除ページ
    """
    template_name = 'booking/booking_delete.html'
    model = Schedule

    success_url = reverse_lazy("booking:calendar") #削除成功したらカレンダーへ

class FnishPage(generic.UpdateView):
    template_name = 'booking/update.html'
    model = Schedule
    fields = ['end']

    def form_valid(self, form):
        f_time = datetime.datetime.now().time()
        #print(f_time)
        #予約表の予約終了時間の書き換え
        booking_schedule = form.save(commit=False)
        booking_schedule.end = f_time
        booking_schedule.save()
        #print(self.kwargs.get('pk'))
        for lending_book in Lending_book.objects.filter(booking_id=self.kwargs.get('pk')):
            lending_book_id = lending_book.id
            L_book = Lending_book.objects.get(id=lending_book_id)
            L_book.l_end = f_time
            L_book.save()
        return redirect('booking:calendar')

    def get_success_url(self):
        return redirect('booking:calendar')