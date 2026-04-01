# 🏦 AlkeWallet — Nordic Minimalist v3.0
### Sistema de Gestión Financiera · Django 6.0 + Nordic UI 2025

---

## 📦 ¿Qué es este proyecto?

**AlkeWallet** es una plataforma fintech de alto rendimiento diseñada para la gestión integral de activos personales. Desarrollada sobre **Django 6**, implementa una arquitectura robusta de backend que cumple satisfactoriamente con los requerimientos técnicos de la evaluación ABP, integrando una interfaz de usuario **Premium Nordic Minimalist**.

### ✨ Características Destacadas (Backend & UI)
*   **Gestión Multiusuario:** Aislamiento total de datos; cada usuario gestiona exclusivamente sus propias cuentas y transacciones.
*   **Lógica de Negocio Transaccional:** Actualización automática de saldos y validación de fondos en tiempo real al registrar movimientos.
*   **ORM Avanzado:** Implementación de agregaciones complejas (`Sum`, `Count`), filtros condicionales con `Q` objects y optimización de consultas via `select_related`.
*   **Motor de Búsqueda ABP:** Filtro multicriterio por titular, tipo de operación, descripción y rangos de fecha.
*   **Seguridad y Sesiones:** Acceso protegido en el 100% de las rutas mediante `LoginRequiredMixin` y decoradores.
*   **Nordic UI Core:** Estética basada en el minimalismo escandinavo con soporte nativo para **Dark Mode**.

---

## 🏗️ Requerimientos Técnicos Evaluados (Backend)

### 📊 1. Manipulación de Datos con ORM
*   **Agregaciones en Dashboard:** Uso de `aggregate()` para calcular ahorros totales, ingresos mensuales y gastos consolidados, ofreciendo una visión clara de la salud financiera.
*   **Consultas Condicionales:** Empleo de objetos `Q` en la vista de búsqueda para realizar consultas `OR` (ej: buscar simultáneamente en titular y descripción).
*   **Optimización N+1:** Uso de `select_related('cuenta')` en listados para minimizar las consultas a la base de datos y mejorar la latitud de respuesta.

### 🔐 2. Seguridad y Acceso
*   **Autenticación Requerida:** Todas las vistas (CBVs y FBVs) exigen un usuario autenticado.
*   **Autorización / Multitenancy:** Sobrescritura de `get_queryset()` en todas las vistas de lista y detalle para asegurar que un usuario nunca pueda acceder a datos de terceros mediante manipulación de URLs.

### 🚀 3. CRUD y Lógica de Aplicación
*   **CRUD Completo:** Implementación de `CreateView`, `UpdateView`, `DeleteView` y `DetailView` para las entidades core (`Cuenta` y `Transaccion`).
*   **Seeding Automático:** Inclusión del comando personalizado `poblar_db` para generar un entorno de prueba realista de forma instantánea.
*   **Integridad Referencial:** Relación `ForeignKey` con `on_delete=CASCADE` configurada para mantener la consistencia histórica de los registros.

---

## 🗂️ Estructura del Proyecto
```text
alkewallet/
├── alkewallet/             # Configuración del proyecto
│   ├── settings/           # Configuración modular (Base, Dev, Prod)
│   ├── urls.py
│   └── wsgi.py
├── wallet/                 # Aplicación principal (Dominio)
│   ├── management/commands/ poblar_db.py  # Script de seeding de datos
│   ├── static/wallet/css/  # Sistema de diseño Nordic v3.0
│   ├── templates/wallet/   # Plantillas Django con herencia de bloques
│   ├── views.py            # Lógica de negocio, ORM y Controladores
│   ├── models.py           # Definición de Entidades y Esquema DB
│   └── forms.py            # Validaciones de entrada y formularios Django
├── db.sqlite3              # Base de datos pre-cargada
├── manage.py
└── requirements.txt
```

---

## 🧱 Modelo de Datos Detallado

### `Cuenta` (Propietario de Fondos)
| Atributo | Tipo Django | Propósito |
|---|---|---|
| `usuario` | `ForeignKey(User)` | Asociación al sistema de Auth de Django |
| `nombre_titular`| `CharField(100)` | Denominación legal de la cuenta |
| `numero_cuenta` | `CharField(unique)` | Identificador bancario irrepetible |
| `saldo` | `DecimalField` | Almacenamiento de precisión para dinero |

### `Transaccion` (Registro Histórico)
| Atributo | Tipo Django | Propósito |
|---|---|---|
| `cuenta` | `ForeignKey` | Cuenta origen del movimiento |
| `cuenta_destino`| `ForeignKey` | Requerido para transferencias bancarias |
| `tipo` | `Choices` | Depósito / Retiro / Transferencia |
| `monto` | `DecimalField` | Valor absoluto de la transacción |
| `fecha` | `DateTimeField` | Timestamp automático de la operación |

---

## 🚀 Instalación y Despliegue

### 1. Clonar el repositorio
```bash
git clone https://github.com/javiersandovaltap-beep/abp7-alkewallet.git
cd alkewallet
```

### 2. Preparar Entorno
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

### 3. Base de Datos y Datos Iniciales
```bash
# Crear el archivo .env basado en .env.example
cp .env.example .env

# Ejecutar migraciones e inicio
python manage.py migrate
python manage.py createsuperuser
python manage.py poblar_db     # Genera datos de prueba automáticos
```

### 4. Ejecución
```bash
python manage.py runserver
```
Acceso: `http://127.0.0.1:8000/`

---

## 🛠️ Evolución Técnica: Problemas Resueltos

### 🌑 1. Modo Oscuro con Persistencia
**Problema:** El cambio de tema se perdía al recargar la página.  
**Solución:** Implementación de script `localStorage` en `base.html` y variables CSS con `@media (prefers-color-scheme)` y selectores `[data-theme="dark"]`.

### 📉 2. Estadísticas en el Dashboard
**Problema:** Los totales de ingresos/gastos no se calculaban dinámicamente.  
**Solución:** Lógica de agregación con `Sum` y `Case/When` en `views.py` para separar flujos monetarios mensuales sin múltiples queries.

### 🧩 3. Error de Bloque Duplicado (`TemplateSyntaxError`)
**Problema:** Varias páginas arrojaban error por etiquetas `{% endblock %}` redundantes.  
**Solución:** Auditoría completa de templates y estandarización del cierre de bloques para evitar errores de renderizado en Django 6.

### 📱 4. Responsividad Crítica en Buscador
**Problema:** En dispositivos móviles, los elementos del buscador se sobreponían o desaparecían.  
**Solución:** Migración a un sistema de cuadrícula flexible (Grid) y eliminación de márgenes negativos obsoletos.

---

## 🔍 Motor de Búsqueda y Filtros (Punto Clave ABP)

El sistema de búsqueda avanzada en `/transacciones/buscar/` implementa una lógica de filtrado dinámico que combina múltiples criterios:

*   **Búsqueda Textual:** Uso de `Q(descripcion__icontains=q) | Q(cuenta__nombre_titular__icontains=q)` para realizar búsquedas insensibles a mayúsculas en múltiples campos.
*   **Filtros de Tipo:** Filtrado exacto por naturaleza del movimiento (Depósito, Retiro, Transferencia).
*   **Rangos de Fecha:** Implementación de `fecha__date__gte` y `fecha__date__lte` para permitir auditorías financieras por periodos temporales específicos.
*   **Seguridad en Búsqueda:** El queryset está restringido al usuario en sesión mediante `Transaccion.objects.filter(cuenta__usuario=self.request.user)`, garantizando que el buscador no exponga datos de otros clientes.

---

## 🛠️ Lógica de Negocio y Transaccionalidad

A diferencia de un CRUD simple, **AlkeWallet** gestiona la integridad de los fondos en el servidor:
1.  **Validación de Tipo:** Al procesar un formulario de transacción, el backend identifica el impacto en el balance.
2.  **Aritmética Automatizada:** Los depósitos suman al saldo, mientras que retiros y transferencias restan, todo gestionado mediante el método `form_valid` en los controladores (Views).
3.  **Transferencias de Doble Entrada:** Al realizar una transferencia, el sistema actualiza simultáneamente el saldo de la cuenta origen y la cuenta destino en una operación atómica.

---

## ❓ Preguntas de Cierre

**1. ¿Qué modelos definiste y por qué?**  
Se definieron `Cuenta` (para representar balances y titulares) y `Transaccion` (para registrar movimientos). Esta separación es fundamental para normalizar la base de datos y permitir un historial de auditoría claro por cada cuenta.

**2. ¿Cómo garantizaste la seguridad de los datos entre usuarios?**  
Se implementó un sistema de **Multi-tenancy** a nivel de aplicación sobrescribiendo el método `get_queryset()` en todas las Clase-Based Views, asegurando que cada consulta a la base de datos esté filtrada por `request.user`.

**3. ¿Qué métodos del ORM fueron vitales para las estadísticas?**  
El uso de `.aggregate()` con `Sum` y `Count` permitió obtener totales financieros de forma eficiente directamente desde el motor de base de datos, evitando cargar registros innecesarios en la memoria de Python.

---

## 📋 Checklist de Requerimientos ABP

- [x] **Modelos:** Definición de campos, tipos y restricciones según requerimiento.
- [x] **Relaciones:** Uso de `ForeignKey` con integridad referencial (`CASCADE`).
- [x] **ORM:** Consultas complejas con filtros (`Q`), ordenamiento y agregaciones.
- [x] **CRUD:** Operaciones completas para Cuentas y Transacciones.
- [x] **Buscador:** Filtro avanzado con criterios de texto, tipo y fechas.
- [x] **Seguridad:** Protección de rutas y aislamiento de datos por usuario.
- [x] **Seed:** Comando `poblar_db` para carga masiva de datos iniciales.

---
*AlkeWallet Nordic v3.0 — Acceso a Datos con Django · Alke Financial · 2026*