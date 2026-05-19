# SAP — Ampliación y modificación masiva de materiales

Herramienta interna para generar los archivos `.txt` que se cargan en SAP para ampliar o modificar materiales de forma masiva. Reemplaza el proceso manual de completar cada vista en SAP uno a uno.

---

## Instalación y arranque

**Requisitos:** Python 3.10 o superior.

```powershell
# Desde la carpeta del proyecto
python -m pip install streamlit pandas
python -m streamlit run app.py
```

El navegador se abre en `http://localhost:8501`.
Para detener la aplicación: `Ctrl + C` en la terminal.

---

## Flujo general de la aplicación

La app tiene **dos pasos** antes de llegar al formulario:

```
Paso 1 — Configurar operación
  └── Elegir tipo de operación (centros logísticos / sucursales / modificación)
  └── Elegir tipo de material (ZMED, ZNOM, ZINS, etc.)
  └── Pegar los números de material (MATNR) desde Excel

Paso 2 — Completar vistas
  └── Cada vista del .txt es una pestaña independiente
  └── Los campos se propagan entre pestañas automáticamente
  └── En cada pestaña hay un botón "Generar .txt"

Descarga
  └── ZIP con un .txt por cada vista generada
```

---

## Paso 1 — Configuración

### Tipo de operación

| Operación | Descripción | Archivos que genera |
|---|---|---|
| **Ampliación centros logísticos** | Amplía materiales a A110, A120 y/o A130 | Hasta 8 `.txt` |
| **Ampliación sucursales** | Amplía materiales a los ~70 centros de sucursales | 2–3 `.txt` |
| **Modificación datos básicos** | Modifica campos de materiales existentes | 1 `.txt` |

### Tipo de material

Determina qué campos están disponibles, qué valores son fijos, qué vistas se generan y a qué centros aplica.

| Tipo | Descripción |
|---|---|
| ZMED | Medicamentos — tiene gestión de lotes, caducidad, perfil serie |
| ZNOM | Nomenclados — similar a ZMED sin lotes ni caducidad |
| ZINS | Insumos — sin MRP completo |
| ZSER\_C | Servicios con compra en sucursales |
| ZSER\_NC | Servicios sin compra en sucursales |
| ZNOA | No almacenables — va a los 3 centros logísticos y a todas las sucursales |
| ZCOM | Componentes — solo a A130, sin valoración |

### Ingreso de MATNR

Copiá una columna de Excel con los números de material y pegala directamente en el área de texto. La app toma cada línea como un material distinto. También podés escribirlos manualmente, uno por línea.

---

## Paso 2 — Vistas (pestañas)

Cada pestaña corresponde a una vista de SAP y a un `.txt` de salida. Podés navegar libremente entre pestañas: **los datos que ingresás en una pestaña se conservan al cambiar a otra**.

### Datos básicos

Campos que completa el usuario (según tipo de material):

| Campo | Técnico | Tipo | Aplica a |
|---|---|---|---|
| Descripción | MAKTX | Texto libre | Todos |
| Grupo de productos | MATKL | Texto libre | CL |
| Jerarquía de productos | PRDHA | Texto libre | CL |
| Volumen | VOLUM | Número | ZMED, ZNOM, ZCOM |
| Partición | SPART | Desplegable | ZNOM (S2/S3) |
| Texto largo | TEXTO\_LARGO | Texto libre | Todos (default = descripción) |
| Estado del material | MSTAE | Checkbox | Todos |

**Checkbox MSTAE:**
- ✅ Marcado → material activo, se escribe `/` en el `.txt`
- ☐ Desmarcado → material bloqueado, campo vacío en el `.txt`

### Datos de centro

Para **centros logísticos**: muestra una sección por cada centro (A110, A120, A130) con los campos editables de ese centro.

Campos que el usuario puede editar:

| Campo | Técnico | Tipo |
|---|---|---|
| Grupo de compra | EKGRP | Desplegable |
| Indicador de impuestos | TAXIM | Desplegable (1–7) |

El resto (DISMM, DISPO, MTVFP, LADGR, LGFSB, etc.) son valores fijos del sistema visibles en el expander "Valores fijos".

Para **sucursales**: muestra el mapa completo de centros (WERKS → KOKRS / PRCTR). El usuario no edita nada; la app genera una fila por material por cada sucursal del mapa.

### Cadenas de distribución

Un campo editable:

| Campo | Técnico | Tipo |
|---|---|---|
| Grupo de imputación | KTGRM | Desplegable |

La estructura de cadenas (organizaciones de venta 3001 y 1001, canales, centros suministradores) es fija por tipo de material y se muestra como tabla de referencia.

### Clasificación fiscal, Datos de previsión, Lugares de almacenamiento, Área planif. MRP, Datos de valoración

Estas pestañas son **completamente automáticas**. El usuario solo las usa para revisar los datos que se van a generar y para hacer click en "Generar" si quiere descargar solo esa vista.

---

## Función "Aplicar a todos"

Cada campo editable tiene un botón **"↕ Aplicar a todos"** (visible cuando hay más de un material). Completás el valor para el primer material, hacés click, y ese valor se copia a todos los demás. Útil cuando todos los materiales tienen el mismo EKGRP, TAXIM o KTGRM.

---

## Generación y descarga

El botón **"⚙️ Generar .txt"** está disponible en cada pestaña. Antes de generar muestra una barra de estado:

| Estado | Significado |
|---|---|
| 🟢 Verde | Todos los campos obligatorios están completos |
| 🟡 Amarillo | Hay campos opcionales vacíos, se puede generar igual |
| 🔴 Rojo | Hay errores que bloquean la generación |

Al generar se descarga un **ZIP** con un `.txt` por cada vista. El ZIP incluye solo las vistas que aplican al tipo de material elegido.

### Formato de los `.txt`

Los archivos respetan exactamente el formato que SAP espera para la carga masiva:

- **Separador:** tabulación (TAB)
- **Fila 1:** nombres de columna en español
- **Fila 2:** nombres técnicos SAP (MATNR, MAKTX, etc.)
- **Fila 3 en adelante:** datos de los materiales
- **Encoding:** UTF-8
- **Fin de línea:** CRLF (Windows)

### Archivos generados por flujo y tipo de material

**Ampliación centros logísticos:**

| Archivo | ZMED | ZNOM | ZINS | ZSER\_C | ZSER\_NC | ZNOA | ZCOM |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Datos\_basicos.txt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Datos\_de\_centro.txt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cadenas\_de\_distribucion.txt | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Clasificacion\_fiscal.txt | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Datos\_de\_prevision.txt | ✅ | ✅ | — | — | — | — | — |
| Lugares\_de\_almacenamiento.txt | ✅ | ✅ | ✅ | — | — | — | ✅ |
| Area\_planific\_nec.txt | ✅ | ✅ | — | — | — | — | — |
| Datos\_valoracion.txt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |

**Ampliación sucursales:** Datos\_basicos.txt + Datos\_de\_centro.txt + Datos\_valoracion.txt (solo ZINS)

**Modificación datos básicos:** Datos\_basicos.txt

---

## Estructura del proyecto

```
sap_app/
├── app.py              Interfaz de usuario (Streamlit)
├── config.py           Toda la configuración: tipos de material,
│                       valores fijos, opciones de campos, mapa de centros
├── txt_generator.py    Generación de cada archivo .txt
└── requirements.txt    Dependencias Python
```

### config.py — dónde tocar si algo cambia

**Cambiar un valor fijo** (ej: PLIFZ de A130 en ZNOM):
```python
# TIPOS_MATERIAL["ZNOM"]["CL_centros"] → el dict con "WERKS": "A130"
"PLIFZ": "5"   # cambiar acá
```

**Ampliar las opciones de un desplegable** (ej: nuevo grupo de compra):
```python
# En OPCIONES al tope del archivo
"EKGRP_ZMED_ZNOM": ["001","002","003","004","005","008"],  # agregar "008"
```

**Agregar una sucursal nueva al mapa:**
```python
# En CENTRO_BENEFICIO_MAP
"0077": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
```

**Agregar un nuevo tipo de material:** copiar una entrada existente de `TIPOS_MATERIAL` y ajustar sus valores.

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje base |
| Streamlit | Interfaz web — formularios, tablas editables, descarga |
| pandas | Manejo de tablas y timestamps |
| zipfile (stdlib) | Empaquetado de los `.txt` en un ZIP descargable |
| io.BytesIO (stdlib) | Generación de archivos en memoria, sin escritura en disco |

---

## Preguntas frecuentes

**¿Puedo generar solo una vista sin completar todas las demás?**
Sí. El botón "Generar" en cada pestaña genera el ZIP con todas las vistas del flujo usando lo que haya hasta ese momento. Los campos vacíos opcionales se generan vacíos en el `.txt`.

**¿Qué pasa si pego los MATNR con espacios o filas vacías?**
La app los limpia automáticamente. Solo procesa líneas con contenido.

**¿Puedo volver a cambiar el tipo de material después de cargar los MATNR?**
Sí, usando el botón "← Nueva operación". Eso reinicia la sesión y limpia los datos cargados.

**¿Los `.txt` generados son iguales a los que armaba manualmente?**
Sí. El formato (TAB, CRLF, UTF-8, dos filas de encabezado) es idéntico al estándar usado para la carga masiva en SAP.
