from django import forms
from .models import *
from .models import Reserva

from .models import Viaje

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
        fields = ['nombre', 'correo', 'telefono', 'direccion']


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'correo', 'telefono', 'direccion', 'fecha_inicio', 'fecha_fin', 'comentarios']
        
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }
        
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
