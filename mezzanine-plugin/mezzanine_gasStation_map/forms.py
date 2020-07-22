from django.forms import ModelForm, ModelChoiceField, DateInput, DateTimeField,Form
from mezzanine_gasStation_map.models import plotModel

class Plot_Form(ModelForm):
     class Meta:
        model = plotModel
        fields = ['state','initial_date','end_date']
        widgets = {
            'initial_date': DateInput(attrs={'class':'datepicker form-control py-4 px-4','data-provide':'datepicker'}),
            'end_date': DateInput(attrs={'class':'datepicker form-control py-4 px-4' , 'data-provide':'datepicker'})
        }
#class DateForm(Form):
#    date = DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
