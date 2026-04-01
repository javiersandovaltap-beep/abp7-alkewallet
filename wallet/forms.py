from django import forms
from .models import Cuenta, Transaccion


class CuentaForm(forms.ModelForm):
    class Meta:
        model  = Cuenta
        exclude = ['usuario']
        widgets = {
            'nombre_titular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez'
            }),
            'numero_cuenta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 0001-0234-5678'
            }),
            'saldo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'tipo_cuenta': forms.Select(attrs={
                'class': 'form-select',
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_saldo(self):
        saldo = self.cleaned_data.get('saldo')
        if saldo is not None and saldo < 0:
            raise forms.ValidationError('El saldo no puede ser negativo.')
        return saldo


class TransaccionForm(forms.ModelForm):
    class Meta:
        model  = Transaccion
        fields = '__all__'
        widgets = {
            'cuenta': forms.Select(attrs={
                'class': 'form-select',
            }),
            'cuenta_destino': forms.Select(attrs={
                'class': 'form-select',
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select',
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pago de servicios...',
            }),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')
        return monto

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        monto = cleaned_data.get('monto')
        cuenta = cleaned_data.get('cuenta')
        cuenta_destino = cleaned_data.get('cuenta_destino')

        if monto and cuenta:
            if tipo in ['retiro', 'transferencia'] and cuenta.saldo < monto:
                raise forms.ValidationError(f"Fondos insuficientes. Se intentó mover ${monto} pero el saldo es de ${cuenta.saldo}.")

            if tipo == 'transferencia':
                if not cuenta_destino:
                    raise forms.ValidationError("Debes indicar una cuenta de destino para realizar la transferencia.")
                if cuenta == cuenta_destino:
                    raise forms.ValidationError("No puedes transferir a la misma cuenta de origen.")
            elif cuenta_destino:
                cleaned_data['cuenta_destino'] = None

        return cleaned_data
