from django.forms import ModelForm, NumberInput, TextInput, Textarea, URLInput

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

from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }