from django import forms

CHOICES=[('Inflow','Inflow'),
         ('Outflow','Outflow')]

class ExpenseForm(forms.Form):
	title = forms.CharField()
	amount = forms.IntegerField()
	in_or_out = forms.ChoiceField(choices = CHOICES, widget = forms.RadioSelect)
	category = forms.CharField()
	date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
