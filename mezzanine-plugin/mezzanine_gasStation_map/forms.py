from django.forms import ModelForm, ModelChoiceField, DateInput, DateTimeField, Form, HiddenInput, NumberInput
from mezzanine_gasStation_map.models import plotModel, calModel

class Plot_Form(ModelForm):
     class Meta:
        model = plotModel
        fields = ['state','initial_date','end_date']
        widgets = {
            'initial_date': DateInput(attrs={'class':'datepicker form-control py-4 px-4','data-provide':'datepicker'}),
            'end_date': DateInput(attrs={'class':'datepicker form-control py-4 px-4' , 'data-provide':'datepicker'})
        }

class Cal_Form(ModelForm):
     class Meta:
        model = calModel
        fields = ['startX','startY','economy','money']
        #widgets = {
        #    'startX' : NumberInput(attrs={ 'disabled': True }),
        #    'startY' : NumberInput(attrs={ 'disabled': True })
        #}
#class DateForm(Form):
#    date = DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
