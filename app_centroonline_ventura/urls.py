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
    path('producto/', views.ProductoListView.as_view(), name='producto_list'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('producto/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_edit'),
    path('producto/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    

    
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedido/nuevo/', views.PedidoCreateView.as_view(), name='pedido_create'),
    path('pedido/<int:pk>/eliminar/', views.PedidoDeleteView.as_view(), name='pedido_delete'),
    # Ventura Market
    path('market/', views.ProductoMarketListView.as_view(), name='productos_market'),
    path('producto/<int:pk>/', views.DetalleProductoView.as_view(), name='detalle_producto'),

    # Home Build
    path('construccion/', views.ProyectoConstruccionListView.as_view(), name='proyectos'),

    # Autenticación y administración
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)