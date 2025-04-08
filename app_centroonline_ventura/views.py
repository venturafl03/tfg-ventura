from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import ReservaForm
from django.views.generic import DetailView, FormView
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Vehiculo, Reserva
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View


# Vistas generales
def principal(request):
    return render(request, 'centroonline/principal.html')

# Vistas para Ventura Motors

class LiberarVehiculoView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        """Solo permite acceso a usuarios staff"""
        return self.request.user.is_staff

    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        vehiculo.reservado = False
        vehiculo.reservado_por = None
        vehiculo.fecha_reserva = None
        vehiculo.save()
        
        messages.success(request, f'Vehículo {vehiculo} liberado correctamente')
        return redirect('listado')  # Redirige al listado de vehículos

class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'centroonline/vehiculos/listado.html'
    context_object_name = 'vehiculos'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(reservado=False)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for vehiculo in context['vehiculos']:
            if vehiculo.reservado:
                vehiculo.reserva_activa = vehiculo.reserva_set.filter(
                    fecha_fin__gte=timezone.now().date()
                ).first()
        return context

class VehiculosReservadosListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'centroonline/vehiculos/reservados.html'
    context_object_name = 'vehiculos'
    
    def get_queryset(self):
        return Vehiculo.objects.filter(reservado=True)

class VehiculoDetailView(DetailView):
    model = Vehiculo
    template_name = 'centroonline/vehiculos/detalle_vehiculo.html'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo = self.object
        
        # Obtener reserva activa si existe
        if vehiculo.reservado:
            context['reserva_activa'] = vehiculo.reserva_set.filter(
                fecha_fin__gte=timezone.now().date()
            ).first()
        
        # Control de acceso para vehículos reservados
        context['mostrar_detalles_completos'] = (
            not vehiculo.reservado or 
            self.request.user.is_staff or
            (self.request.user.is_authenticated and 
             vehiculo.reservado_por == self.request.user)
        )
        
        return context

class TestDriveCreateView(LoginRequiredMixin, CreateView):
    model = TestDrive
    form_class = TestDriveForm
    template_name = 'centroonline/vehiculos/test_drive.html'
    success_url = reverse_lazy('listado')

    def form_valid(self, form):
        # Asegura que el usuario y el vehículo se asignen correctamente al formulario
        form.instance.usuario = self.request.user
        form.instance.vehiculo = get_object_or_404(Vehiculo, pk=self.kwargs['pk'])
        return super().form_valid(form)
    
from .forms import ReservaForm  # Asegúrate de tener este formulario

class ReservarVehiculoView(LoginRequiredMixin, FormView):
    template_name = 'centroonline/vehiculos/reservar_vehiculo.html'
    form_class = ReservaForm
    success_url = reverse_lazy('listado')  # Ajusta según tu URL de éxito

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo = get_object_or_404(Vehiculo, pk=self.kwargs['vehiculo_id'])
        context['vehiculo'] = vehiculo
        return context

    def form_valid(self, form):
        vehiculo = get_object_or_404(Vehiculo, pk=self.kwargs['vehiculo_id'])
        
        # Crear la reserva
        reserva = form.save(commit=False)
        reserva.vehiculo = vehiculo
        reserva.save()
        
        # Actualizar estado del vehículo
        vehiculo.reservado = True
        vehiculo.reservado_por = self.request.user
        vehiculo.fecha_reserva = timezone.now()
        vehiculo.save()
        
        return super().form_valid(form)

class ReservaConfirmadaView(DetailView):
    model = Vehiculo
    template_name = 'centroonline/vehiculos/reserva_confirmada.html'
    context_object_name = 'vehiculo'

    def get_object(self):
        vehiculo_id = self.kwargs.get('vehiculo_id')
        return get_object_or_404(Vehiculo, pk=vehiculo_id)

    def post(self, request, *args, **kwargs):
        vehiculo = self.get_object()
        # Aquí puedes agregar lógica adicional para manejar la reserva, como guardar los datos en un modelo
        # Por ejemplo, podrías guardar un nuevo registro de reserva:
        reserva = Reserva.objects.create(
            vehiculo=vehiculo,
            nombre=request.POST.get('nombre'),
            correo=request.POST.get('correo'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion')
        )

        # Redirigir al usuario a una página de confirmación después de la reserva
        return HttpResponseRedirect(reverse('reserva_confirmada', args=[vehiculo.pk]))



# Vistas para Baguetería Ventura
class ProductoListView(ListView):
    model = Producto
    template_name = 'centroonline/bagueteria/menu.html'
    context_object_name = 'productos'

class PedidoCreateView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'centroonline/bagueteria/pedido.html'
    success_url = reverse_lazy('menu_bagueteria')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'centroonline/bagueteria/pedido_detalle.html'



# Vistas para Ventura Market
class ProductoMarketListView(ListView):
    model = ProductoMarket
    template_name = 'centroonline/market/menu.html'
    context_object_name = 'productos'

class DetalleProductoView(DetailView):
    model = Producto
    template_name = 'centroonline/market/detalle_producto.html'
    context_object_name = 'producto'



# Vistas para Home Build
class ProyectoConstruccionListView(ListView):
    model = ProyectoConstruccion
    template_name = 'centroonline/construccion/proyectos.html'
    context_object_name = 'proyectos'

class ProyectoConstruccionDetailView(DetailView):
    model = ProyectoConstruccion
    template_name = 'centroonline/construccion/detalle_proyecto.html'

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de inicio de sesión después de registrarse
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('principal')  # Redirige a la página principal después de iniciar sesión
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('principal') 