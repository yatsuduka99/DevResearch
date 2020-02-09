import requests
import json
import datetime
from app.logger import logger

"""
  DB項目リスト値
    タプル型にリスト値を設定
"""
EVENT_ATTNDC_LIST = [
    ('1', '〇△×'),
    ('2', '◎〇△×'),
    ('3', '〇×')
]
ANSWER_LIST = [
    ('0', '-'),
    ('1', '◎'),
    ('2', '〇'),
    ('3', '△'),
    ('4', '×'),
]
"""
  定数
"""
INVAITE_MAX_COUNT = 99
EVENT_DATE_MAX_COUNT = 4


class WebApiRequest:
    """ __ はプライベートとして扱われる"""
    __BASE_URI = ('https://pzz2yg2vta.execute-api.'
                  'ap-northeast-1.amazonaws.com/api/')
    __response_status = '0'
    __response_text = ''
    __request_headers = {}

    """ HTTPリクエストステータス取得 """

    # @logger(func_name="WebApiRequest.get_request_status")
    def get_request_status(self):
        return self.__response_status

    """ HTTPリクエストテキスト取得 """

    # @logger(func_name="WebApiRequest.get_request_text")
    def get_request_text(self):
        return self.__response_text

    """ HTTPリクエスト GETメソッド """

    # @logger(func_name="WebApiRequest.request_get_method")
    def request_get_method(self, uri):
        request_uri = self.__BASE_URI + uri
        response = requests.get(
            request_uri,
            headers=self.__request_headers)
        self.__response_status = str(response.status_code)
        self.__response_text = response.text
        json_dict = json.loads(self.__response_text)
        return json_dict

    """ HTTPリクエスト POSTメソッド """

    # @logger(func_name="WebApiRequest.request_post_method")
    def request_post_method(self, uri, body_json_dict):
        request_uri = self.__BASE_URI + uri
        response = requests.post(
            request_uri,
            headers=self.__request_headers,
            json=body_json_dict)
        self.__response_status = str(response.status_code)
        self.__response_text = response.text

    """ HTTPリクエスト PUTメソッド """

    # @logger(func_name="WebApiRequest.request_put_method")
    def request_put_method(self, uri, body_json_dict):
        request_uri = self.__BASE_URI + uri
        response = requests.put(
            request_uri,
            headers=self.__request_headers,
            json=body_json_dict)
        self.__response_status = str(response.status_code)
        self.__response_text = response.text

    """ HTTPリクエスト DELETEメソッド """

    # @logger(func_name="WebApiRequest.request_delete_method")
    def request_delete_method(self, uri):
        request_uri = self.__BASE_URI + uri
        response = requests.delete(
            request_uri,
            headers=self.__request_headers)
        self.__response_status = str(response.status_code)
        self.__response_text = response.text


class ApiScheduleCheck(WebApiRequest):
    """イベントID取得"""

    @logger(func_name="ApiScheduleCheck.get_event_id")
    def get_event_id(self):
        return WebApiRequest.request_get_method(
            self,
            'event-id')

    """イベント取得（全件）"""

    @logger(func_name="ApiScheduleCheck.get_event_all")
    def get_event_all(self):
        return WebApiRequest.request_get_method(
            self,
            'event')

    """イベント作成"""

    @logger(func_name="ApiScheduleCheck.create_event")
    def create_event(self, body_json_dict):
        return WebApiRequest.request_post_method(
            self,
            'event',
            body_json_dict)

    """イベント取得"""

    @logger(func_name="ApiScheduleCheck.get_event")
    def get_event(self, event_id):
        return WebApiRequest.request_get_method(
            self,
            'event/' + event_id)

    """イベント更新"""

    @logger(func_name="ApiScheduleCheck.update_event")
    def update_event(self, event_id, body_json_dict):
        return WebApiRequest.request_put_method(
            self,
            'event/' + event_id, body_json_dict)

    """イベント削除"""

    @logger(func_name="ApiScheduleCheck.delete_event")
    def delete_event(self, event_id):
        return WebApiRequest.request_delete_method(
            self,
            'event/' + event_id)

    """パスワード認証確認"""

    @logger(func_name="ApiScheduleCheck.is_auth_event_password")
    def is_auth_event_password(self, request, event_id):
        get_json = self.get_event(str(event_id))

        session_event_password_check = \
            request.session.pop('event_password_check', None)
        if session_event_password_check is None:
            if get_json['EVENT_PW'] != '':
                return True
        return False

    """招待者取得"""

    @logger(func_name="ApiScheduleCheck.get_invite")
    def get_invite(self, event_id):
        return WebApiRequest.request_get_method(
            self,
            'event/' + event_id + '/invite')

    """招待者更新（全件）"""

    @logger(func_name="ApiScheduleCheck.update_invite_all")
    def update_invite_all(self, event_id, body_json_dict):
        return WebApiRequest.request_post_method(
            self,
            'event/' + event_id + '/invite',
            body_json_dict
        )

    """招待者更新"""

    @logger(func_name="ApiScheduleCheck.update_invite")
    def update_invite(self, event_id, invite_id, body_json_dict):
        return WebApiRequest.request_post_method(
            self,
            'event/' + event_id + '/invite/' + invite_id,
            body_json_dict
        )

    """出欠取得"""

    @logger(func_name="ApiScheduleCheck.get_attendance")
    def get_attendance(self, event_id):
        return WebApiRequest.request_get_method(
            self,
            'event/' + event_id + '/attendance')

    """出欠更新（全件）"""

    @logger(func_name="ApiScheduleCheck.update_attendance_all")
    def update_attendance_all(self, event_id, body_json_dict):
        return WebApiRequest.request_post_method(
            self,
            'event/' + event_id + '/attendance',
            body_json_dict
        )

    """出欠更新"""

    @logger(func_name="ApiScheduleCheck.update_attendance")
    def update_attendance(self, event_id, invite_id, body_json_dict):
        return WebApiRequest.request_post_method(
            self,
            'event/' + event_id + '/attendance/' + invite_id,
            body_json_dict
        )

    @logger(func_name="ApiScheduleCheck.get_attendance_data")
    def get_attendance_data(self, event_id=None, invite_id=None):
        """各種DB取得"""
        json_dict_api_event = self.get_event(str(event_id))
        json_dict_api_invite = self.get_invite(str(event_id))
        json_dict_api_attendance = self.get_attendance(str(event_id))

        """イベント情報編集"""
        # 出欠表のヘッダも作成
        list_table_header = []
        list_event_date = []
        json_dict_event = json_dict_api_event
        # 回答選択肢
        for i in EVENT_ATTNDC_LIST:
            if json_dict_event['EVENT_ATTNDC_ID'] in i:
                json_dict_event['EVENT_ATTNDC_DISPLAY'] = i[1]
        # 候補日
        item_count_event_date = EVENT_DATE_MAX_COUNT
        for idx in reversed(range(1, EVENT_DATE_MAX_COUNT + 1)):
            # 値が存在する最後の項目までを画面に表示するのでそれ以降は削除する
            item_key = 'EVENT_DATE' + str(idx)
            if json_dict_event[item_key] == '':
                del json_dict_event[item_key]
                item_count_event_date -= 1
            else:
                break
        for idx in range(1, item_count_event_date + 1):
            item_key = 'EVENT_DATE' + str(idx)
            # リストへの追加(コード値)
            list_event_date.append(json_dict_event[item_key])
            if json_dict_event[item_key] != '':
                temp_date = datetime.datetime.strptime(
                    json_dict_event[item_key],
                    '%Y-%m-%d')
                json_dict_event[item_key] = \
                    '{0:%Y/%m/%d (%a)}'.format(temp_date)
            # リストへの追加(表示用)
            list_table_header.append(json_dict_event[item_key])

        """招待者編集"""
        item_count_invite = INVAITE_MAX_COUNT
        list_invite = []
        if 'error_message' not in json_dict_api_invite:
            """データが存在する場合"""
            for idx in reversed(range(1, INVAITE_MAX_COUNT + 1)):
                # 値が存在する最後の項目までを画面に表示するのでそれ以降は削除する
                item_key = 'NAME' + str(idx).zfill(2)
                if json_dict_api_invite[item_key] == '':
                    del json_dict_api_invite[item_key]
                    item_count_invite -= 1
                else:
                    break
            if invite_id is None:
                # 招待者全員分
                for idx in range(1, item_count_invite + 1):
                    item_key = 'NAME' + str(idx).zfill(2)
                    if item_key in list(json_dict_api_invite):
                        list_invite.append(json_dict_api_invite[item_key])
            else:
                # 招待者個別
                item_key = 'NAME' + str(invite_id).zfill(2)
                if item_key in list(json_dict_api_invite):
                    list_invite.append(json_dict_api_invite[item_key])

        """出欠編集"""
        # 出欠表のデータを作成
        # 事前に招待者のリストはパラメータによって全員 or 個別
        # になっているのでそちら次第でできるデータは変化する
        lists_table_data = []
        lists_attendance = []
        for invite_idx, invite_val in enumerate(list_invite):
            list_table_data = [invite_val]
            list_attendance = []
            for event_date_idx, event_date_val in enumerate(list_table_header):
                if invite_id is None:
                    item_key = 'ANSWER' \
                               + str(invite_idx + 1).zfill(2) \
                               + '_' + str(event_date_idx + 1)
                else:
                    item_key = 'ANSWER' \
                               + str(invite_id).zfill(2) \
                               + '_' + str(event_date_idx + 1)

                # 回答
                if item_key in list(json_dict_api_attendance):
                    if json_dict_api_attendance[item_key] == '':
                        json_dict_api_attendance[item_key] = '0'
                    # リストへの追加(コード値)
                    list_attendance.append(json_dict_api_attendance[item_key])
                    for i in ANSWER_LIST:
                        if json_dict_api_attendance[item_key] in i:
                            json_dict_api_attendance[item_key] = i[1]
                    # リストへの追加(表示値)
                    list_table_data.append(json_dict_api_attendance[item_key])
            # リスト配列への追加
            lists_table_data.append(list_table_data)
            lists_attendance.append(list_attendance)

        context = {
            'event': json_dict_event,
            'list_table_header': list_table_header,
            'lists_table_data': lists_table_data,
            'list_event_date': list_event_date,
            'list_invite': list_invite,
            'lists_attendance': lists_attendance
        }
        return context
