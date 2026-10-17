from django import forms
from django.utils import timezone

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            "customer_name",
            "email",
            "phone",
            "reservation_date",
            "reservation_time",
            "party_size",
            "special_requests",
        )
        widgets = {
            "customer_name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TelInput(attrs={"placeholder": "+254 700 000 000", "autocomplete": "tel"}),
            "reservation_date": forms.DateInput(attrs={"type": "date"}),
            "reservation_time": forms.TimeInput(attrs={"type": "time"}),
            "party_size": forms.NumberInput(attrs={"min": 1, "max": 20}),
            "special_requests": forms.Textarea(attrs={"rows": 4, "placeholder": "Allergies, accessibility needs, or other requests (optional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "reservation-input"
        self.fields["reservation_date"].widget.attrs["min"] = timezone.localdate().isoformat()
        self.fields["party_size"].help_text = "For parties larger than 20, please contact us directly."

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data["reservation_date"]
        if reservation_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return reservation_date

    def clean_party_size(self):
        party_size = self.cleaned_data["party_size"]
        if not 1 <= party_size <= 20:
            raise forms.ValidationError("Party size must be between 1 and 20.")
        return party_size

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        digit_count = sum(character.isdigit() for character in phone)
        if digit_count < 7 or digit_count > 15:
            raise forms.ValidationError("Enter a valid phone number with 7 to 15 digits.")
        return phone
