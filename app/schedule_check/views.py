from django.shortcuts import render, redirect
from django.views import generic
from app.schedule_check.models import ApiScheduleCheck
from app.schedule_check.forms import EventEditForm
from app.schedule_check.forms import AttendanceEditForm
import app.schedule_check.models as const
from app.logger import logger
from app.logger import calc_time

"""
スケジュールチェック
"""


class IndexView(generic.TemplateView):
    """トップページ"""
    template_name = "schedule_check/index.html"


class HowToUserView(generic.TemplateView):
    """使い方"""
    template_name = "schedule_check/how_to_user.html"


class EventListView(generic.View):
    """イベント一覧"""
    template_name = "schedule_check/event_list.html"

    @calc_time(func_name="EventListView.get")
    def get(self, request, *args, **kwargs):
        """イベント情報をDB取得"""
        api = ApiScheduleCheck()
        get_jsons = api.get_event_all()

        """配列内辞書のキーでソート"""
        # キーは自前で作成してからソートしている
        for get_json in get_jsons:
            get_json['SORT_DATA'] = str(get_json['EVENT_ID']).zfill(10)
        get_jsons = sorted(get_jsons,
                           reverse=True,
                           key=lambda x: x['SORT_DATA'])

        context = {'dts': get_jsons}
        return render(request, self.template_name, context)


class EventDetailListView(generic.View):
    """イベント一覧詳細"""
    template_name = "schedule_check/event_list_detail.html"

    @calc_time(func_name="EventDetailListView.get")
    def get(self, request, *args, **kwargs):
        """イベント情報をDB取得"""
        api = ApiScheduleCheck()
        get_jsons = api.get_event(str(kwargs['event_id']))

        context = {'dt': get_jsons}
        return render(request, self.template_name, context)


class EventCreateView(generic.View):
    """イベント新規作成"""
    get_template_name = "schedule_check/event_create.html"
    post_redirect_name = "schedule_check:event_list"

    @calc_time(func_name="EventCreateView.get")
    def get(self, request, *args, **kwargs):
        f = EventEditForm()
        context = {
            'form': f,
        }
        return render(request, self.get_template_name, context)

    @calc_time(func_name="EventCreateView.post")
    def post(self, request, *args, **kwargs):
        api = ApiScheduleCheck()
        json_dict = api.get_event_id()
        event_id = json_dict['EVENT_ID']

        """画面のPOSTデータを取得"""
        f = EventEditForm(request.POST)
        """DB更新"""
        post_json = {
            'EVENT_ID': event_id,
            'EVENT_NAME': f.data['event_name'],
            'EVENT_DATE1': f.data['event_date1'],
            'EVENT_DATE2': f.data['event_date2'],
            'EVENT_DATE3': f.data['event_date3'],
            'EVENT_DATE4': f.data['event_date4'],
            'EVENT_DSCRPT': f.data['event_dscrpt'],
            'EVENT_PW': f.data['event_pw'],
            'EVENT_ATTNDC_ID': f.data['event_attndc_id'],
        }
        api.create_event(post_json)
        """リダイレクト"""
        return redirect(self.post_redirect_name)


class EventEditView(generic.View):
    """イベント編集"""
    get_template_name = "schedule_check/event_edit.html"
    post_redirect_name = "schedule_check:event_list"

    @calc_time(func_name="EventEditView.get")
    def get(self, request, *args, **kwargs):
        """パスワード認証確認"""
        api = ApiScheduleCheck()
        if api.is_auth_event_password(request, kwargs['event_id']):
            """リダイレクト"""
            return redirect('schedule_check:event_password',
                            event_id=kwargs['event_id'],
                            next_page='schedule_check:event_edit')

        """画面のクラス生成する際に初期値を設定"""
        get_json = api.get_event(str(kwargs['event_id']))
        f = EventEditForm(
            initial={
                'event_name': get_json['EVENT_NAME'],
                'event_date1': get_json['EVENT_DATE1'],
                'event_date2': get_json['EVENT_DATE2'],
                'event_date3': get_json['EVENT_DATE3'],
                'event_date4': get_json['EVENT_DATE4'],
                'event_dscrpt': get_json['EVENT_DSCRPT'],
                'event_pw': get_json['EVENT_PW'],
                'event_attndc_id': get_json['EVENT_ATTNDC_ID'],
            }
        )
        context = {
            'dt': get_json,
            'form': f,
        }
        return render(request, self.get_template_name, context)

    @calc_time(func_name="EventEditView.post")
    def post(self, request, *args, **kwargs):
        """画面のPOSTデータを取得"""
        f = EventEditForm(request.POST)
        """DB更新"""
        post_json = {
            'EVENT_ID': str(kwargs['event_id']),
            'EVENT_NAME': f.data['event_name'],
            'EVENT_DATE1': f.data['event_date1'],
            'EVENT_DATE2': f.data['event_date2'],
            'EVENT_DATE3': f.data['event_date3'],
            'EVENT_DATE4': f.data['event_date4'],
            'EVENT_DSCRPT': f.data['event_dscrpt'],
            'EVENT_PW': f.data['event_pw'],
            'EVENT_ATTNDC_ID': f.data['event_attndc_id'],
        }
        api = ApiScheduleCheck()
        api.update_event(str(kwargs['event_id']), post_json)
        """リダイレクト"""
        return redirect(self.post_redirect_name)


class EventDeleteView(generic.View):
    """イベント削除"""

    @calc_time(func_name="EventDeleteView.get")
    def get(self, request, *args, **kwargs):
        """パスワード認証確認"""
        api = ApiScheduleCheck()
        if api.is_auth_event_password(request, kwargs['event_id']):
            """リダイレクト"""
            return redirect('schedule_check:event_password',
                            event_id=kwargs['event_id'],
                            next_page='schedule_check:event_delete')

        """イベント情報 DB削除"""
        api.delete_event(str(kwargs['event_id']))
        """リダイレクト"""
        return redirect('schedule_check:event_list')


class EventPasswordAuth(generic.View):
    """パスワード認証"""

    @calc_time(func_name="EventPasswordAuth.get")
    def get(self, request, *args, **kwargs):
        context = {'EVENT_ID': str(kwargs['event_id'])}
        return render(request, 'schedule_check/event_edit_login.html', context)

    @calc_time(func_name="EventPasswordAuth.post")
    def post(self, request, *args, **kwargs):
        api = ApiScheduleCheck()
        get_json = api.get_event(str(kwargs['event_id']))
        f = request.POST
        if f['input_password'] == get_json['EVENT_PW']:
            # パスワード認証成功
            # Django標準機能のセッションを作成しておく。リダイレクト先で削除
            request.session['event_password_check'] = 'ok'
        else:
            # パスワード認証失敗
            context = {
                'EVENT_ID': str(kwargs['event_id']),
                'ERROR_MESSAGE': 'パスワードが異なります。'}
            return render(request,
                          'schedule_check/event_edit_login.html',
                          context)

        """リダイレクト"""
        # 遷移先はパラメータより
        if kwargs['next_page'] == 'schedule_check:event_edit':
            return redirect(kwargs['next_page'],
                            event_id=kwargs['event_id'])
        elif kwargs['next_page'] == 'schedule_check:event_delete':
            return redirect(kwargs['next_page'],
                            event_id=kwargs['event_id'])
        elif kwargs['next_page'] == 'schedule_check:invite':
            return redirect(kwargs['next_page'],
                            event_id=kwargs['event_id'])
        else:
            return redirect('schedule_check:event_list_detail',
                            event_id=kwargs['event_id'])


class EventUrlView(generic.View):
    """イベントURL"""
    template_name = "schedule_check/event_url.html"

    @calc_time(func_name="EventUrlView.get")
    def get(self, request, *args, **kwargs):
        """イベント情報をDB取得"""
        context = {'EVENT_ID': str(kwargs['event_id'])}
        return render(request, self.template_name, context)


class InviteView(generic.View):
    """イベント招待"""
    get_template_name = "schedule_check/invite.html"
    post_redirect_name = "schedule_check:event_list_detail"

    @calc_time(func_name="InviteView.get")
    def get(self, request, *args, **kwargs):
        """パスワード認証確認"""
        api = ApiScheduleCheck()
        if api.is_auth_event_password(request, kwargs['event_id']):
            """リダイレクト"""
            return redirect('schedule_check:event_password',
                            event_id=kwargs['event_id'],
                            next_page='schedule_check:invite')

        """招待者情報 DB参照"""
        api = ApiScheduleCheck()
        get_json = api.get_invite(str(kwargs['event_id']))
        if 'error_message' not in get_json:
            """データが存在する場合"""
            item_dict = {}
            item_count = const.INVAITE_MAX_COUNT
            for idx in reversed(range(1, const.INVAITE_MAX_COUNT + 1)):
                # 値が存在する最後の項目までを画面に表示するのでそれ以降は削除する
                item_key = 'NAME' + str(idx).zfill(2)
                if get_json[item_key] == '':
                    del get_json[item_key]
                    item_count -= 1
                else:
                    break
            # 画面に表示する値をセットする
            for idx in (range(1, item_count + 1)):
                item_key = 'NAME' + str(idx).zfill(2)
                form_key = 'invite[' + str(idx - 1) + ']'
                item_dict[form_key] = get_json[item_key]
            context = {
                'EVENT_ID': str(kwargs['event_id']),
                'ITEM_COUNT': str(item_count + 1),
                'dt': item_dict
            }
        else:
            context = {
                'EVENT_ID': str(kwargs['event_id']),
                'ITEM_COUNT': str(0),
            }
        return render(request, self.get_template_name, context)

    @calc_time(func_name="InviteView.post")
    def post(self, request, *args, **kwargs):
        """画面のPOSTデータを取得"""
        f = request.POST

        """DB更新"""
        api = ApiScheduleCheck()
        post_json = {'EVENT_ID': str(kwargs['event_id'])}
        # APIはINVAITE_MAX_COUNT個まで受け付けるのでFormに値が
        # 存在する項目のみをAPIパラメータとする
        for idx in range(1, const.INVAITE_MAX_COUNT + 1):
            item_key = 'NAME' + str(idx).zfill(2)
            form_key = 'invite[' + str(idx - 1) + ']'
            if form_key in f:
                post_json[item_key] = f[form_key]
        api.update_invite_all(str(kwargs['event_id']), post_json)

        """リダイレクト"""
        return redirect(self.post_redirect_name,
                        event_id=kwargs['event_id'])


class AttendanceListView(generic.View):
    """イベント参加確認"""
    get_template_name = "schedule_check/attendance.html"

    @calc_time(func_name="AttendanceListView.get")
    def get(self, request, *args, **kwargs):
        api = ApiScheduleCheck()
        context = api.get_attendance_data(kwargs['event_id'], None)
        return render(request, self.get_template_name, context)


class AttendanceEditView(generic.View):
    """イベント参加編集"""
    get_template_name = "schedule_check/attendance_edit.html"
    post_redirect_name = "schedule_check:attendance"

    @calc_time(func_name="AttendanceEditView.get")
    def get(self, request, *args, **kwargs):
        """各種情報をDB取得"""
        api = ApiScheduleCheck()
        dt = api.get_attendance_data(kwargs['event_id'],
                                     kwargs['invite_id'])

        """回答選択肢の作成"""
        # 「-」選択肢は回答選択肢内に存在しないため固定で追加
        answer_lists = [('0', '-')]
        val = dt['event']['EVENT_ATTNDC_ID']
        for attndc_dt in const.EVENT_ATTNDC_LIST:
            if val == attndc_dt[0]:
                for answer_dt in const.ANSWER_LIST:
                    if answer_dt[1] in attndc_dt[1]:
                        answer_lists.append(answer_dt)

        """初期値表示"""
        f = AttendanceEditForm.create_form(
            range_index=len(dt['lists_attendance'][0]),
            init_val=dt['lists_attendance'],
            answer_list=answer_lists
        )
        context = {
            'form': f,
            'dt': dt,
            'INVITE_ID': str(kwargs['invite_id'])
        }
        return render(request, self.get_template_name, context)

    @calc_time(func_name="AttendanceEditView.post")
    def post(self, request, *args, **kwargs):
        """画面のPOSTデータを取得"""
        f = AttendanceEditForm(request.POST)

        """DB更新"""
        api = ApiScheduleCheck()
        post_json = {
            'EVENT_ID': str(kwargs['event_id']),
            'INVITE_ID': str(kwargs['invite_id'])
        }
        for idx in range(1, const.EVENT_DATE_MAX_COUNT + 1):
            item_key = 'ANSWER_' + str(idx)
            if item_key in f.data:
                post_json[item_key] = f.data[item_key]
        api.update_attendance(str(kwargs['event_id']),
                              str(kwargs['invite_id']),
                              post_json)

        """リダイレクト"""
        return redirect(self.post_redirect_name,
                        event_id=kwargs['event_id'])
