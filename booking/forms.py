#from django import forms
from django.forms import ModelForm, Form
from booking.models import Schedule, Lending_book

class BookForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ("end", "user")
        widgets = {}

class LendingForm(ModelForm):
    class Meta:
        model = Lending_book
        fields = ("l_place",)
        widgets = {}