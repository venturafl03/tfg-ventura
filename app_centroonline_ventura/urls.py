from django.urls import path, include  # Añade include
from django.contrib import admin  # Importa admin
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import LiberarVehiculoView

urlpatterns = [
    # General
    path('', views.principal, name='principal'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),

    # Ventura Motors
    path('vehiculos/', views.VehiculoListView.as_view(), name='listado'),
    path('vehiculos/<int:pk>/', views.VehiculoDetailView.as_view(), name='detalle_vehiculo'),
    path('vehiculos/<int:pk>/test-drive/', views.TestDriveCreateView.as_view(), name='test_drive'),
    path('reservar/<int:vehiculo_id>/', views.ReservarVehiculoView.as_view(), name='reservar_vehiculo'),
    path('reserva_confirmada/<int:vehiculo_id>/', views.ReservaConfirmadaView.as_view(), name='reserva_confirmada'),
    path('vehiculos/reservados/', views.VehiculosReservadosListView.as_view(), name='vehiculos_reservados'),
     path('vehiculos/<int:pk>/liberar/', LiberarVehiculoView.as_view(), name='liberar_vehiculo'),

    # Baguetería Ventura
    path('bagueteria/', views.ProductoListView.as_view(), name='menu_bagueteria'),
    path('bagueteria/pedido/', views.PedidoCreateView.as_view(), name='nuevo_pedido'),
    path('bagueteria/pedido/<int:pk>/', views.PedidoDetailView.as_view(), name='detalle_pedido'),

    # Ventura Market
    path('market/', views.ProductoMarketListView.as_view(), name='market'),
    path('producto/<int:pk>/', views.DetalleProductoView.as_view(), name='detalle_producto'),
    # Home Build
    path('construccion/', views.ProyectoConstruccionListView.as_view(), name='proyectos'),
    path('construccion/detalle/<int:pk>/', views.ProyectoConstruccionDetailView.as_view(), name='detalle_proyecto'),


   #perfumeria 
   path('perfumerias/', views.PerfumeriaListView.as_view(), name='perfumeria'),

  # libreria 
   path('estudio/', views.ProductoEstudioListView.as_view(), name='estudio'),
   path('estudio/detalle/<int:pk>/', views.ProductoEstudioDetailView.as_view(), name='detalle_producto_estudio'),

    # viajes
    path('viaje/', views.ViajeListView.as_view(), name='viaje'),
    path('viaje/<int:pk>/', views.ViajeDetailView.as_view(), name='detalle_viaje'),
    path('crear/', views.ViajeCreateView.as_view(), name='crear_viaje'),
    path('editar/<int:pk>/', views.ViajeUpdateView.as_view(), name='editar_viaje'),
    path('eliminar/<int:pk>/', views.ViajeDeleteView.as_view(), name='eliminar_viaje'),
    # Autenticación y administración

    path('accounts/', include('django.contrib.auth.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)