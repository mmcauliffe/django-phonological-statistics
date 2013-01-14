
from django import forms

class ResetForm(forms.Form):
    reset = forms.BooleanField(initial=True)

class AnalyzeForm(forms.Form):
    segments = forms.CharField(label="Segment string")
    nostress = forms.BooleanField(label="Ignore stress?",required=False,initial=False)
