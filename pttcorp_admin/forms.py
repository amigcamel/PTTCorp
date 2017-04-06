#-*-coding:utf-8-*-
from django import forms
from .models import UpdateLogModel  

class UpdateLogModelForm(forms.ModelForm):
    class Meta:
        model = UpdateLogModel
        widgets = {
                   'update_message': forms.Textarea(attrs={'required':'required', 'class':'form-control'})
                  } 


