from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.utils import timezone


from .models import Cuenta, Transaccion
from .forms import CuentaForm, TransaccionForm


# ── INICIO / DASHBOARD ─────────────────────────────────────────────────────
@login_required
def home(request):
    # ✅ FIX: filtrado por usuario activo
    stats_cuentas = Cuenta.objects.filter(usuario=request.user).aggregate(
        total=Count('id'),
        activas=Count('id', filter=Q(activa=True)),
        saldo_total=Sum('saldo'),
    )

    # Estadísticas mensuales (ingresos y gastos del mes actual)
    now = timezone.now()
    txns_mes = Transaccion.objects.filter(
        cuenta__usuario=request.user,
        fecha__year=now.year,
        fecha__month=now.month,
    )
    ingresos_mes = txns_mes.filter(tipo='deposito').aggregate(total=Sum('monto'))['total'] or 0
    gastos_mes = txns_mes.filter(tipo__in=['retiro', 'transferencia']).aggregate(total=Sum('monto'))['total'] or 0

    ultimas_transacciones = (
        Transaccion.objects.filter(cuenta__usuario=request.user)
        .select_related('cuenta')
        .order_by('-fecha')[:5]
    )

    ultimas_cuentas = (
        Cuenta.objects.filter(usuario=request.user)
        .order_by('-fecha_creacion')[:4]
    )

    context = {
        'total_cuentas':         stats_cuentas['total'] or 0,
        'cuentas_activas':       stats_cuentas['activas'] or 0,
        'saldo_total':           stats_cuentas['saldo_total'] or 0,
        'ingresos_mes':          ingresos_mes,
        'gastos_mes':            gastos_mes,
        'total_transacciones':   Transaccion.objects.filter(cuenta__usuario=request.user).count(),
        'ultimas_transacciones': ultimas_transacciones,
        'ultimas_cuentas':       ultimas_cuentas,
    }
    return render(request, 'wallet/home.html', context)


# ── CUENTAS ────────────────────────────────────────────────────────────────
class CuentaListView(LoginRequiredMixin, ListView):
    model = Cuenta
    template_name = 'wallet/cuenta_list.html'
    context_object_name = 'cuentas'
    paginate_by = 10

    def get_queryset(self):
        return Cuenta.objects.filter(usuario=self.request.user).order_by('nombre_titular')


class CuentaDetailView(LoginRequiredMixin, DetailView):
    model = Cuenta
    template_name = 'wallet/cuenta_detail.html'
    context_object_name = 'cuenta'

    def get_queryset(self):
        return Cuenta.objects.filter(usuario=self.request.user)


class CuentaCreateView(LoginRequiredMixin, CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'wallet/cuenta_form.html'
    success_url = reverse_lazy('wallet:cuenta_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, '✅ Cuenta creada exitosamente.')
        return super().form_valid(form)


class CuentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'wallet/cuenta_form.html'
    success_url = reverse_lazy('wallet:cuenta_list')

    def get_queryset(self):
        return Cuenta.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '✏️ Cuenta actualizada.')
        return super().form_valid(form)


class CuentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cuenta
    template_name = 'wallet/cuenta_confirm_delete.html'
    success_url = reverse_lazy('wallet:cuenta_list')

    def get_queryset(self):
        return Cuenta.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.warning(self.request, '🗑️ Cuenta eliminada.')
        return super().form_valid(form)


# ── TRANSACCIONES ──────────────────────────────────────────────────────────
class TransaccionListView(LoginRequiredMixin, ListView):
    model = Transaccion
    template_name = 'wallet/transaccion_list.html'
    context_object_name = 'transacciones'
    paginate_by = 10

    def get_queryset(self):
        return Transaccion.objects.filter(cuenta__usuario=self.request.user).select_related('cuenta').order_by('-fecha')


class TransaccionDetailView(LoginRequiredMixin, DetailView):
    model = Transaccion
    template_name = 'wallet/transaccion_detail.html'
    context_object_name = 'transaccion'

    def get_queryset(self):
        return Transaccion.objects.filter(cuenta__usuario=self.request.user)


class TransaccionCreateView(LoginRequiredMixin, CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'wallet/transaccion_form.html'
    success_url = reverse_lazy('wallet:transaccion_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cuenta'].queryset = Cuenta.objects.filter(usuario=self.request.user)
        return form

    def form_valid(self, form):
        transaccion = form.instance
        monto = transaccion.monto
        
        if transaccion.tipo == 'deposito':
            transaccion.cuenta.saldo += monto
        elif transaccion.tipo == 'retiro':
            transaccion.cuenta.saldo -= monto
        elif transaccion.tipo == 'transferencia':
            transaccion.cuenta.saldo -= monto
            transaccion.cuenta_destino.saldo += monto
            transaccion.cuenta_destino.save()
            
        transaccion.cuenta.save()
        messages.success(self.request, '✅ Transacción registrada y fondos actualizados.')
        return super().form_valid(form)


class TransaccionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'wallet/transaccion_form.html'
    success_url = reverse_lazy('wallet:transaccion_list')

    def get_queryset(self):
        return Transaccion.objects.filter(cuenta__usuario=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cuenta'].queryset = Cuenta.objects.filter(usuario=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, '✏️ Transacción actualizada.')
        return super().form_valid(form)


class TransaccionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaccion
    template_name = 'wallet/transaccion_confirm_delete.html'
    success_url = reverse_lazy('wallet:transaccion_list')

    def get_queryset(self):
        return Transaccion.objects.filter(cuenta__usuario=self.request.user)

    def form_valid(self, form):
        messages.warning(self.request, '🗑️ Transacción eliminada.')
        return super().form_valid(form)


# ── BÚSQUEDA / FILTRO ─────────────────────────────────────────────────────
class TransaccionBuscarView(LoginRequiredMixin, ListView):
    model = Transaccion
    template_name = 'wallet/transaccion_buscar.html'
    context_object_name = 'transacciones'
    paginate_by = 20

    def get_queryset(self):
        # ✅ FIX: sin parámetros activos → queryset vacío
        # (el template muestra "usá los filtros" y no hay datos detrás)
        params = {
            k: v for k, v in self.request.GET.items()
            if v.strip()
        }
        if not params:
            return Transaccion.objects.none()

        qs = Transaccion.objects.filter(cuenta__usuario=self.request.user).select_related('cuenta')

        # Filtro por titular o descripción
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(descripcion__icontains=q) |
                Q(cuenta__nombre_titular__icontains=q)
            )

        # Filtro por tipo
        tipo = self.request.GET.get('tipo', '').strip()
        if tipo:
            qs = qs.filter(tipo=tipo)

        # ✅ FIX: filtros de fecha implementados
        fecha_desde = self.request.GET.get('fecha_desde', '').strip()
        if fecha_desde:
            qs = qs.filter(fecha__date__gte=fecha_desde)

        fecha_hasta = self.request.GET.get('fecha_hasta', '').strip()
        if fecha_hasta:
            qs = qs.filter(fecha__date__lte=fecha_hasta)

        return qs.order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ✅ FIX: devuelve los 4 filtros al template para mantener valores
        context['q']           = self.request.GET.get('q', '')
        context['tipo']        = self.request.GET.get('tipo', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context