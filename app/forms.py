from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from app.models import Video


class UserDownloadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FieldWithButtons("url", Submit("download", "Загрузить")),
        )

    class Meta:
        model = Video
        fields = {
            "url",
        }
        labels = {
            "url": "Введите URL:",
        }
