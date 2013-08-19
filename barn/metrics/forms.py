from django.forms import DateInput


class RecordedInput(DateInput):
    input_type = 'date'
