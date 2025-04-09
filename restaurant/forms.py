from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['restaurant', 'reservation_time', 'number_of_people', 'special_requests']
        widgets = {
            'reservation_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'restaurant': forms.Select(attrs={'class': 'form-control'})
        }