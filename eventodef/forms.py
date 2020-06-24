from django import forms
from .models import *

class UploadFileForm(forms.Form):
    file = forms.FileField(label='', help_text= 'Planilha .xlsx' )
    deltae = forms.FloatField(label='', help_text='Tempo entre dados')
    ptot = forms.FloatField(label='', help_text='Precipitação total mínima', required=False)
    deltat = forms.IntegerField(label='', help_text='Tempo de discretização', required=False)
    imed = forms.FloatField(label='', help_text='Intensidade média minima', required=False)

    