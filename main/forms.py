from django.forms import ModelForm, NumberInput, TextInput, Textarea

from main.models import Interest

class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = [
            "title",
            "description",
            "since",
        ]

        labels = {
            "title": "Nama Interest",
            "description": "Deskripsi Interest",
            "since": "Tahun mulai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Minum Kopi",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan minatmu",
                    "rows": 3,
                }
            ),
            "since": NumberInput(
                attrs={
                    "placeholder": "2026",
                    "min": 1,
                    "max": 9999,
                }
            ),
        }