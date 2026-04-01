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

### 5. `/login/` devolvía 404
**Causa:** La ruta de login no estaba en `urls.py`.  
**Solución:**
```python
from django.contrib.auth import views as auth_views
path('login/', auth_views.LoginView.as_view(), name='login'),
```

### 6. `block content` duplicado en template
**Causa:** Al pegar código se duplicó `{% block content %}`.  
**Síntoma:** `TemplateSyntaxError: 'block' tag with name 'content' appears more than once`.  
**Solución:** Cada template debe tener exactamente una apertura y un cierre del bloque.

### 7. Dark Mode — pérdida de tema al recargar
**Causa:** El estado del tema no persistía entre navegaciones.  
**Solución:** Script en `base.html` con `localStorage` y variables CSS con
`@media (prefers-color-scheme)` y selector `[data-theme="dark"]`.

### 8. Responsividad en el buscador (mobile)
**Causa:** Elementos del buscador se superponían en pantallas pequeñas.  
**Solución:** Migración a sistema de grilla flexible y eliminación de márgenes negativos.

### 9. `saldo_promedio` calculado pero no usado
**Causa:** `Avg('saldo')` en `aggregate()` nunca entraba al contexto.  
**Solución:** Se eliminó el import de `Avg` y el cálculo innecesario.

### 10. `numero_cuenta` faltaba en el seed `poblar_db`
**Causa:** Al agregar el campo al modelo, el comando seed no se actualizó.  
**Solución:** Agregar `numero_cuenta` único a cada entrada de `cuentas_data`.

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

### Sobre los Modelos

**1. ¿Qué modelos definiste y por qué elegiste esos?**  
`Cuenta` y `Transaccion`. Una wallet necesita representar los contenedores
de dinero (cuentas con titular, tipo y saldo) y los movimientos sobre ellos
(transacciones con tipo, monto y fecha). Separarlos normaliza la base de datos
y permite un historial de auditoría claro por cada cuenta sin duplicar datos.

**2. ¿Qué tipo de relación usaste y por qué esa y no otra?**  
`ForeignKey` de `Transaccion` hacia `Cuenta` — relación muchos a uno.
Una cuenta puede tener muchas transacciones, pero cada transacción pertenece
a exactamente una cuenta. `ManyToMany` no aplica porque una transacción no
pertenece a varias cuentas simultáneamente. `OneToOne` no aplica porque
una cuenta tiene múltiples transacciones.

**3. ¿Qué valor le pusiste a `on_delete` y por qué?**  
`CASCADE`. Al eliminar una cuenta, sus transacciones históricas quedan
huérfanas sin significado financiero, por lo que deben eliminarse
automáticamente para mantener la consistencia de los datos.

### Sobre el ORM

**4. ¿Qué métodos del ORM usaste para cada operación CRUD?**

- **Crear:** `form.save()` en `CreateView` → ejecuta `INSERT`
- **Leer:** `.all()`, `.get(pk=pk)`, `.select_related('cuenta')`, `.order_by()`
- **Actualizar:** `form.save()` en `UpdateView` → ejecuta `UPDATE`
- **Eliminar:** `objeto.delete()` en `DeleteView` → ejecuta `DELETE`
- **Estadísticas:** `.aggregate(Count('id'), Sum('saldo'))`

**5. ¿Qué método usaste en la vista de filtro/búsqueda?**  
`.filter()` con objetos `Q()` para condiciones `OR` entre campos de distintos
modelos. Se encadenan múltiples `.filter()` para condiciones `AND`
(tipo + rango de fechas).

**6. ¿Cuál es la diferencia entre `.get()` y `.filter()`?**  
`.get()` retorna exactamente **un** objeto o lanza excepción
(`DoesNotExist` si no existe, `MultipleObjectsReturned` si hay más de uno).
Se usa cuando el resultado es único, como buscar por PK en `DetailView`.  
`.filter()` siempre retorna un `QuerySet` —puede estar vacío—, ideal para
listas y búsquedas donde el número de resultados es variable.

### Sobre las Migraciones

**7. ¿Qué pasaría si modificás un modelo sin generar una nueva migración?**  
La clase Python y la tabla SQL quedan desincronizadas. Django lanzaría
`OperationalError: no such column` al intentar consultar o guardar datos,
porque el campo existe en el modelo pero no en la base de datos real.
Este error ocurrió exactamente durante el desarrollo al agregar `numero_cuenta`
sin aplicar la migración correctamente.

**8. ¿Dónde se almacenan los archivos de migración y para qué sirven?**  
En `wallet/migrations/`. Son el historial versionado de cambios al esquema
de la DB. Permiten reproducir la estructura exacta en cualquier entorno
(desarrollo, producción, CI/CD) y revertir cambios con
`python manage.py migrate <app> <número_de_migración>`.

### Sobre la Arquitectura

**9. ¿Por qué la lógica de DB debe estar en las vistas y no en los templates?**  
Los templates solo deben **renderizar** datos ya preparados. Incluir lógica
de base de datos en templates rompe la separación MTV (Model-Template-View),
hace imposible escribir tests unitarios sobre esa lógica y mezcla
responsabilidades de presentación con acceso a datos. Django mismo refuerza
esta separación: los templates no tienen acceso directo al ORM.

**10. ¿Cuál es el flujo completo de una solicitud en Django?**
Usuario hace clic / escribe URL

urls.py busca el patrón coincidente

View asociada es invocada

View consulta modelos a través del ORM

ORM genera SQL y lo ejecuta contra SQLite

ORM retorna objetos Python a la view

View construye el contexto y llama al template

Template renderiza HTML con los datos

Django retorna la respuesta HTTP al navegador

El navegador muestra la página al usuario



---

## 📋 Checklist de entrega

- [x] Proyecto ejecuta con `runserver` sin errores
- [x] Modelos con campos, tipos y restricciones correctas
- [x] Relación `ForeignKey` con `on_delete=CASCADE`
- [x] Migraciones aplicadas sin errores
- [x] CRUD completo de **Cuentas** desde templates propios
- [x] CRUD completo de **Transacciones** desde templates propios
- [x] Template de búsqueda/filtro con ORM (`Q()`, `.filter()`, fechas)
- [x] Todas las URLs nombradas y funcionando
- [x] Autenticación requerida en todas las vistas
- [x] Dashboard con estadísticas (`Count`, `Sum`)
- [x] Comando `poblar_db` con datos de prueba
- [x] Django Admin configurado
- [x] Templates responsive mobile-first con Bootstrap 5
- [x] Dark Mode implementado con variables CSS
- [x] `db.sqlite3` incluido en la entrega
- [x] Preguntas de cierre respondidas en este documento

---

## 📦 requirements.txt
django>=6.0
django-debug-toolbar



---

*ABP Módulo 7 — Acceso a Datos con Django · Alke Financial · 2026*