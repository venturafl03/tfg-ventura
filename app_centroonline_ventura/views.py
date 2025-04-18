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
from django.views.generic import ListView, TemplateView


# Vistas generales
def principal(request):
    return render(request, 'centroonline/principal.html')


from .forms import RegistroForm 

class RegistroView(CreateView):
    form_class = RegistroForm 
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')

# Vistas para Ventura Motors

class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'centroonline/vehiculos/reservar_vehiculo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculo'] = get_object_or_404(Vehiculo, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        vehiculo = get_object_or_404(Vehiculo, pk=self.kwargs['pk'])
        
        # Verificar solapamiento de fechas
        reservas_existentes = Reserva.objects.filter(
            vehiculo=vehiculo,
            fecha_fin__gte=form.cleaned_data['fecha_inicio'],
            fecha_inicio__lte=form.cleaned_data['fecha_fin']
        ).exists()
        
        if reservas_existentes:
            messages.error(self.request, 'El vehículo ya tiene reservas en esas fechas')
            return self.form_invalid(form)
            
        reserva = form.save(commit=False)
        reserva.vehiculo = vehiculo
        reserva.usuario = self.request.user
        reserva.save()
        
        # Actualizar estado del vehículo
        vehiculo.reservado = True
        vehiculo.reservado_por = self.request.user
        vehiculo.fecha_reserva = timezone.now()
        vehiculo.reserva_activa = reserva
        vehiculo.save()
        
        messages.success(self.request, 'Reserva confirmada exitosamente')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listado_vehiculos')
 
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
    context_object_name = 'vehiculo'

    def post(self, request, *args, **kwargs):
        vehiculo = self.get_object()
        
        if vehiculo.reservado:
            messages.error(request, f"El vehículo {vehiculo.marca} {vehiculo.modelo} ya está reservado.")
            return self.get(request, *args, **kwargs)
        
        vehiculo.reservado = True
        vehiculo.reservado_por = request.user
        vehiculo.fecha_reserva = timezone.now()
        vehiculo.save()
        
        messages.success(request, f"¡El vehículo {vehiculo.marca} {vehiculo.modelo} ha sido reservado con éxito por {request.user.get_full_name()}.")
        
        return self.get(request, *args, **kwargs) 
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

class ReservarVehiculoView(FormView):
    template_name = 'centroonline/vehiculos/reservar_vehiculo.html'  # Template del formulario
    form_class = ReservaForm
    success_url = reverse_lazy('listado')  # Redirige a la página de listado después de la reserva

    def dispatch(self, request, *args, **kwargs):
        # Obtener el vehículo a reservar
        self.vehiculo = get_object_or_404(Vehiculo, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Verificar si el vehículo ya está reservado
        if self.vehiculo.reservado:
            messages.error(self.request, 'Este vehículo ya está reservado.')
            return redirect('listado')  # Redirige al listado si ya está reservado

        # Guardar la reserva
        reserva = form.save(commit=False)
        reserva.vehiculo = self.vehiculo
        reserva.usuario = self.request.user
        reserva.save()

        # Actualizar el estado del vehículo
        self.vehiculo.reservado = True
        self.vehiculo.reservado_por = self.request.user
        self.vehiculo.fecha_reserva = reserva.fecha_inicio
        self.vehiculo.fecha_fin_reserva = reserva.fecha_fin
        self.vehiculo.save()

        # Mostrar mensaje de éxito
        messages.success(self.request, f'¡Reserva realizada con éxito para {self.vehiculo.marca} {self.vehiculo.modelo}!')
        return HttpResponseRedirect(self.success_url)  # Redirige a la página de listado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculo'] = self.vehiculo  # Pasar el vehículo al contexto del template
        return context


class ReservaConfirmadaView(DetailView):
    model = Vehiculo
    template_name = 'centroonline/vehiculo/reserva_confirmada.html'
    context_object_name = 'vehiculo'

    def get_object(self):
        vehiculo_id = self.kwargs.get('vehiculo_id')
        return get_object_or_404(Vehiculo, pk=vehiculo_id)

    def post(self, request, *args, **kwargs):
        vehiculo = self.get_object()
 
        reserva = Reserva.objects.create(
            vehiculo=vehiculo,
            nombre=request.POST.get('nombre'),
            correo=request.POST.get('correo'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion')
        )

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



class CarritoView(View):
    def get(self, request):
        carrito_productos = request.session.get('carrito', [])
        productos = Producto.objects.filter(id__in=carrito_productos)
        
        return render(request, 'centroonline/bagueteria/carrito.html', {'productos': productos})

class AgregarAlCarritoView(View):
    def post(self, request, producto_id):
        carrito = request.session.get('carrito', [])
        if producto_id not in carrito:
            carrito.append(producto_id)
            request.session['carrito'] = carrito  
        return HttpResponseRedirect(reverse('bagueteria:carrito'))

# Vistas para Ventura Market
class ProductoMarketListView(ListView):
    model = ProductoMarket
    template_name = 'centroonline/market/menu.html'
    context_object_name = 'productos'

class DetalleProductoView(DetailView):
    model = Producto
    template_name = 'centroonline/market/detalle_producto.html'
    context_object_name = 'producto'







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


# perfumeria 
class PerfumeriaListView(ListView):
    model = Perfumeria
    template_name = 'centroonline/perfumeria/perfumeria.html'
    context_object_name = 'perfumerias'

    def get_queryset(self):
        queryset = Perfumeria.objects.all()
        genero = self.request.GET.get('genero')
        if genero:
            queryset = queryset.filter(genero=genero)
        return queryset
    

## vista para los libros 
class ProductoEstudioListView(ListView):
    model = ProductoEstudio
    template_name = 'centroonline/libreria/productos.html'
    context_object_name = 'productos'
    paginate_by = 10  
    def get_queryset(self):
        categoria = self.request.GET.get('categoria', None)
        if categoria:
            return ProductoEstudio.objects.filter(categoria=categoria)
        return ProductoEstudio.objects.all()

# Vista para mostrar el detalle de un producto
class ProductoEstudioDetailView(DetailView):
    model = ProductoEstudio
    template_name = 'centroonline/libreria/detalle_producto.html'
    context_object_name = 'producto'




# viajes 
class ViajeListView(ListView):
    model = Viaje
    template_name = 'centroonline/viajes/listar_viajes.html'
    context_object_name = 'viajes'

# Vista para ver los detalles de un viaje específico
class ViajeDetailView(DetailView):
    model = Viaje
    template_name = 'centroonline/viajes/detalle_viaje.html'
    context_object_name = 'viaje'
    success_url = reverse_lazy('viaje')
