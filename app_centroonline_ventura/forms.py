from django import forms
from .models import *
from .models import Reserva

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
        
        labels = {
            'nombre': 'Nombre completo',
            'correo': 'Correo electrónico',
            'telefono': 'Teléfono de contacto',
            'direccion': 'Dirección',
            'fecha_inicio': 'Fecha de inicio de reserva',
            'fecha_fin': 'Fecha de fin de reserva',
            'comentarios': 'Comentarios adicionales',
        }

