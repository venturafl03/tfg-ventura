from django import forms
from .models import *
from .models import Reserva , Usuario
from django.contrib.auth.forms import UserCreationForm
from app_centroonline_ventura.models import Usuario 


from .models import Viaje


class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario 
        fields = ['username', 'password', ]


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ['fecha_test', 'notas']
        widgets = {
            'fecha_test': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['notas']

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'telefono', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().isoformat(),
                'class': 'form-control'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio < timezone.now().date():
                raise forms.ValidationError("No se pueden seleccionar fechas pasadas")
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError("La fecha final debe ser posterior a la inicial")
        
        return cleaned_data


class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione fecha de inicio',
                    'autocomplete': 'off'
                }
            ),
            'fecha_fin': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione fecha de fin',
                    'autocomplete': 'off'
                }
            ),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError(
                    "La fecha de fin debe ser posterior a la fecha de inicio"
                )
        return cleaned_data
