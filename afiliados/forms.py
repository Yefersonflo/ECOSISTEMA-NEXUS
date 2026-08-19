from django import forms
from django.contrib.auth.models import User
from .models import Carpeta, Profile

class CarpetaForm(forms.ModelForm):
    archivo_digital = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'text-xs font-bold text-slate-500'}))

    class Meta:
        model = Carpeta
        fields = ['categoria', 'nombre', 'identificacion', 'modulo', 'estante', 'bandeja', 'cubiculo', 'numero_carpeta']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'w-full p-4 bg-white border-2 border-comfaBlue/20 rounded-2xl font-black text-comfaBlue'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Nombre completo o Razón Social'}),
            'identificacion': forms.TextInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Cédula o NIT'}),
            'modulo': forms.NumberInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Módulo'}),
            'estante': forms.NumberInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Estante'}),
            'bandeja': forms.NumberInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Bandeja'}),
            'cubiculo': forms.NumberInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Cubículo'}),
            'numero_carpeta': forms.NumberInput(attrs={'class': 'w-full p-4 bg-slate-50 border-2 border-comfaBlue/20 rounded-2xl font-bold text-comfaBlue', 'placeholder': 'Número (1-55)', 'min': '1', 'max': '55'}),
        }
