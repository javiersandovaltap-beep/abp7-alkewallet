from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Cuenta(models.Model):
    TIPO_CHOICES = [
        ('ahorro',    'Cuenta de Ahorro'),
        ('corriente', 'Cuenta Corriente'),
        ('vista',     'Cuenta Vista'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuentas')
    nombre_titular = models.CharField(max_length=100)
    email          = models.EmailField(unique=True)
    numero_cuenta = models.CharField(
        max_length=20,
        unique=True,
        default='',          
        help_text='Ej: 0001-2345-6789'
)
    tipo_cuenta    = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='vista'
    )
    saldo          = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    activa         = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_titular} — {self.numero_cuenta}"

    class Meta:
        ordering        = ['-fecha_creacion']
        verbose_name    = 'Cuenta'
        verbose_name_plural = 'Cuentas'


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('deposito',      'Depósito'),
        ('retiro',        'Retiro'),
        ('transferencia', 'Transferencia'),
    ]

    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name='transacciones',   
    )
    cuenta_destino = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name='transferencias_recibidas',
        null=True,
        blank=True,
        help_text='Obligatorio solo para transferencias.',
    )
    tipo  = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,         
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)], 
    )
    
    descripcion = models.CharField(
        max_length=200,
        blank=True,
        default='',
    )
    fecha = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f"{self.get_tipo_display()} ${self.monto} — {self.cuenta.nombre_titular}"

    class Meta:
        ordering        = ['-fecha']
        verbose_name    = 'Transacción'
        verbose_name_plural = 'Transacciones'
        indexes = [
            models.Index(fields=['tipo']),
            models.Index(fields=['-fecha']),
            models.Index(fields=['cuenta', '-fecha']),
        ]