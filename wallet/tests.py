from django.test import TestCase
from django.contrib.auth.models import User
from wallet.models import Cuenta, Transaccion
from wallet.forms import TransaccionForm

class TransaccionFormTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='testuser', password='password123')
        self.cuenta_origen = Cuenta.objects.create(
            usuario=self.usuario,
            nombre_titular='Cuenta Origen',
            email='origen@test.com',
            numero_cuenta='1111-1111',
            saldo=1000.00
        )
        self.cuenta_destino = Cuenta.objects.create(
            usuario=self.usuario,
            nombre_titular='Cuenta Destino',
            email='destino@test.com',
            numero_cuenta='2222-2222',
            saldo=500.00
        )

    def test_fondos_insuficientes(self):
        """No permite retirar más del saldo disponible"""
        form = TransaccionForm(data={
            'cuenta': self.cuenta_origen.id,
            'tipo': 'retiro',
            'monto': 1500.00,
            'descripcion': 'Retiro fallido'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Fondos insuficientes', str(form.errors))

    def test_transferencia_sin_destino(self):
        """Exige una cuenta destino si es transferencia"""
        form = TransaccionForm(data={
            'cuenta': self.cuenta_origen.id,
            'tipo': 'transferencia',
            'monto': 500.00,
            'descripcion': 'Transferencia fallida'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('indicar una cuenta de destino', str(form.errors))

    def test_transferencia_valida(self):
        """Permite transferir fondos de manera correcta y limpia los errores"""
        form = TransaccionForm(data={
            'cuenta': self.cuenta_origen.id,
            'tipo': 'transferencia',
            'monto': 500.00,
            'cuenta_destino': self.cuenta_destino.id,
            'descripcion': 'Transferencia correcta'
        })
        self.assertTrue(form.is_valid())
