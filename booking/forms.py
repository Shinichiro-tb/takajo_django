#from django import forms
from django.forms import ModelForm
from booking.models import Schedule

class BookForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ("end", "user")

        widgets = {}
