from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wallet.models import Cuenta, Transaccion
import random


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar datos existentes antes de poblar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Transaccion.objects.all().delete()
            Cuenta.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            self.stdout.write(self.style.WARNING('🗑️  Datos anteriores eliminados.'))

        # Crear usuarios simulados para pruebas
        admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@alke.com'})
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        test_user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@alke.com'})
        test_user.set_password('test1234')
        test_user.save()

        users = [admin_user, test_user]

        # ✅ FIX: numero_cuenta agregado a cada entrada
        cuentas_data = [
            {
                'nombre_titular': 'Ana González',
                'email':          'ana.gonzalez@email.com',
                'numero_cuenta':  '0001-0000-0001',
                'tipo_cuenta':    'corriente',
                'saldo':          850000,
            },
            {
                'nombre_titular': 'Carlos Muñoz',
                'email':          'carlos.munoz@email.com',
                'numero_cuenta':  '0001-0000-0002',
                'tipo_cuenta':    'ahorro',
                'saldo':          1200000,
            },
            {
                'nombre_titular': 'María Fernández',
                'email':          'maria.fernandez@email.com',
                'numero_cuenta':  '0001-0000-0003',
                'tipo_cuenta':    'vista',
                'saldo':          320000,
            },
            {
                'nombre_titular': 'Jorge Rodríguez',
                'email':          'jorge.rodriguez@email.com',
                'numero_cuenta':  '0001-0000-0004',
                'tipo_cuenta':    'ahorro',
                'saldo':          2500000,
            },
            {
                'nombre_titular': 'Sofía Martínez',
                'email':          'sofia.martinez@email.com',
                'numero_cuenta':  '0001-0000-0005',
                'tipo_cuenta':    'corriente',
                'saldo':          675000,
            },
        ]

        cuentas = []
        for data in cuentas_data:
            cuenta, created = Cuenta.objects.get_or_create(
                email=data['email'],
                defaults={**data, 'usuario': random.choice(users)}
            )
            cuentas.append(cuenta)
            if created:
                self.stdout.write(f'  ✅ Cuenta creada: {cuenta.nombre_titular}')
            else:
                self.stdout.write(f'  ⏭️  Ya existe: {cuenta.nombre_titular}')

        transacciones_data = [
            {'tipo': 'deposito',      'monto': 500000,  'descripcion': 'Depósito inicial'},
            {'tipo': 'deposito',      'monto': 150000,  'descripcion': 'Transferencia recibida'},
            {'tipo': 'retiro',        'monto': 80000,   'descripcion': 'Pago arriendo'},
            {'tipo': 'retiro',        'monto': 35000,   'descripcion': 'Compra supermercado'},
            {'tipo': 'transferencia', 'monto': 200000,  'descripcion': 'Pago servicio'},
            {'tipo': 'deposito',      'monto': 750000,  'descripcion': 'Sueldo mensual'},
            {'tipo': 'retiro',        'monto': 120000,  'descripcion': 'Pago universidad'},
            {'tipo': 'transferencia', 'monto': 50000,   'descripcion': 'Split de cuenta restaurante'},
            {'tipo': 'deposito',      'monto': 300000,  'descripcion': 'Bono de desempeño'},
            {'tipo': 'retiro',        'monto': 45000,   'descripcion': 'Netflix, Spotify y servicios'},
        ]

        for data in transacciones_data:
            cuenta = random.choice(cuentas)
            Transaccion.objects.create(cuenta=cuenta, **data)

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Seed completado: {len(cuentas_data)} cuentas, '
            f'{len(transacciones_data)} transacciones.'
        ))