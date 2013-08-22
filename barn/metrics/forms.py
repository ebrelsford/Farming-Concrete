from datetime import date

from django.forms import DateInput


class RecordedInput(DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, *args, **kwargs):
        try:
            if not attrs or not 'max' in attrs:
                attrs = {}
            attrs['max'] = date.today().isoformat()
        except Exception:
            pass
        super(RecordedInput, self).__init__(attrs=attrs)
