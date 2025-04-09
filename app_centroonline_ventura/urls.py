from django.urls import path, include  
from django.contrib import admin 
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import LiberarVehiculoView
from .views import RegistroView

urlpatterns = [
    # General
    path('', views.principal, name='principal'),
    path('registro/', RegistroView.as_view(), name='registro'),
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
    path('detalle/<int:pk>/', views.ViajeDetailView.as_view(), name='detalle_viaje'),
    # Autenticación y administración

    path('accounts/', include('django.contrib.auth.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)