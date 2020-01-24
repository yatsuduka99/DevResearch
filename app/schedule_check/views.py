from django.shortcuts import render

# Create your views here.

"""
スケジュールチェック
"""


def index(request):
    """トップページ"""

    return render(request, "schedule_check/index.html")


def how_to_user(request):
    """使い方"""

    return render(request, "schedule_check/index.html")


def event_list(request):
    """イベント一覧"""

    context = {}
    return render(request, "schedule_check/index.html", context)


def event_list_detail(request, event_id=None):
    """イベント一覧詳細"""

    context = {}
    return render(request, "schedule_check/index.html", context)


def event_create(request):
    """イベント新規作成"""

    context = {}
    return render(request, "schedule_check/index.html", context)


def event_url(request, event_id=None):
    """イベントURL"""

    context = {}
    return render(request, "schedule_check/index.html", context)


def event_edit(request, event_id=None):
    """イベント編集"""


def event_delete(request, event_id=None):
    """イベント削除"""


def event_password_auth(request, event_id=None, next_page=None):
    """イベントパスワード認証"""


def invite(request, event_id=None):
    """イベント招待"""


def attendance(request, event_id=None):
    """イベント参加確認"""


def attendance_edit(request, event_id=None, invite_id=None):
    """イベント参加編集"""
