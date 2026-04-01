from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    # Inicio / Dashboard
    path('', views.home, name='home'),

    # --- CUENTAS ---
    path('cuentas/', views.CuentaListView.as_view(), name='cuenta_list'),
    path('cuentas/<int:pk>/', views.CuentaDetailView.as_view(), name='cuenta_detail'),
    path('cuentas/nueva/', views.CuentaCreateView.as_view(), name='cuenta_create'),
    path('cuentas/<int:pk>/editar/', views.CuentaUpdateView.as_view(), name='cuenta_update'),
    path('cuentas/<int:pk>/eliminar/', views.CuentaDeleteView.as_view(), name='cuenta_delete'),

    # --- TRANSACCIONES ---
    path('transacciones/', views.TransaccionListView.as_view(), name='transaccion_list'),
    path('transacciones/<int:pk>/', views.TransaccionDetailView.as_view(), name='transaccion_detail'),
    path('transacciones/nueva/', views.TransaccionCreateView.as_view(), name='transaccion_create'),
    path('transacciones/<int:pk>/editar/', views.TransaccionUpdateView.as_view(), name='transaccion_update'),
    path('transacciones/<int:pk>/eliminar/', views.TransaccionDeleteView.as_view(), name='transaccion_delete'),

    # --- BÚSQUEDA (OBLIGATORIA) ---
    path('transacciones/buscar/', views.TransaccionBuscarView.as_view(), name='transaccion_buscar'),
]
