from django import forms
import app.schedule_check.models as const
from app.logger import logger


class EventEditForm(forms.Form):
    event_name = forms.CharField(
        label='イベント名',
        required=True,
        help_text='※必須'
    )
    event_date1 = forms.DateField(
        label='候補日１',
        required=True,
        help_text='※必須',
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    event_date2 = forms.DateField(
        label='候補日２',
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    event_date3 = forms.DateField(
        label='候補日３',
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    event_date4 = forms.DateField(
        label='候補日４',
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    event_dscrpt = forms.CharField(
        label='イベント説明',
        required=False,
        widget=forms.Textarea
    )
    event_pw = forms.CharField(
        label='パスワード',
        required=False,
        widget=forms.PasswordInput(render_value=True),
        strip=False
    )
    event_attndc_id = forms.ChoiceField(
        label='回答選択肢',
        required=True,
        widget=forms.RadioSelect,
        choices=const.EVENT_ATTNDC_LIST
    )


class AttendanceEditForm(forms.Form):
    @staticmethod
    def create_form(range_index, init_val, answer_list, *arg):
        f = forms.Form(*arg)
        for idx in range(1, range_index + 1):
            f.fields['ANSWER_' + str(idx)] = forms.ChoiceField(
                label=idx,
                required=True,
                widget=forms.Select,
                choices=answer_list,
                initial=init_val[0][idx - 1]
            )
        return f
