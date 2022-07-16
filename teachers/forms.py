from django import forms
from datetime import datetime,timedelta


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class QAUploadForm(forms.Form):
    subject = forms.CharField(label='Subject')
    topic = forms.CharField(label = 'Topic')
    doc = forms.FileField(label = 'CSV Upload', allow_empty_file=False)
    start_date = forms.DateField(label = 'Start Date',widget=DatePickerInput)
    start_time = forms.TimeField(label = 'Start Time',widget=TimePickerInput)
    end_date = forms.DateField(label='End Date',widget=DatePickerInput)
    end_time = forms.TimeField(label = 'End Time',widget=TimePickerInput)
    duration = forms.IntegerField(label = 'Duration(in min)')
    neg_mark = forms.IntegerField(label = "Negative Marks Percentage")
    password = forms.CharField(label='Exam Password',widget=forms.PasswordInput,max_length=20)
    proctor_type = forms.ChoiceField(label = 'Proctoring Type',widget=forms.RadioSelect, choices=[('0', 'Automatic Monitoring'), ('1', 'Live Monitoring')])

    def validate_end_date(form, field):
        if field.data < form.start_date:
            raise forms.ValidationError("End date must not be earlier than start date.")

    def validate_end_time(form, field):
        start_date_time = datetime.strptime(str(form.start_date) + " " + str(form.start_time),
                                            "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        end_date_time = datetime.strptime(str(form.end_date) + " " + str(field.data),
                                          "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        if start_date_time >= end_date_time:
            raise forms.ValidationError("End date time must not be earlier/equal than start date time")

    def validate_start_date(form, field):
        if datetime.strptime(str(form.start_date) + " " + str(form.start_time),
                             "%Y-%m-%d %H:%M:%S") < datetime.now():
            raise forms.ValidationError("Start date and time must not be earlier than current")