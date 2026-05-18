# SAP - Ampliación masiva de materiales

Herramienta para generar archivos Excel de carga masiva en SAP (MM17 / LSMW).

## Estructura del proyecto

```
sap_ampliacion/
├── app.py                        # Interfaz Streamlit (punto de entrada)
├── config.py                     # Configuración central: tipos de material, valores fijos, mapa de centros
├── requirements.txt
└── generators/
    ├── __init__.py
    ├── utils.py                  # Helpers: escribir_excel, construir_datos_basicos, etc.
    ├── centros_logisticos.py     # Flujo 1: ampliación centros logísticos
    ├── sucursales.py             # Flujo 2: ampliación sucursales
    └── modificacion.py           # Flujo 3: modificación datos básicos
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Flujos disponibles

### 1. Ampliación centros logísticos
- Tipos de material: ZMED, ZNOM, ZINS, ZSER_C, ZSER_NC, ZNOA, ZCOM
- Genera hojas: Datos básicos, Datos de centro, Cadenas de distribución,
  Clasificación fiscal, Datos de previsión, Lugares de almacenamiento,
  Área planific.nec., Datos de valoración
- **Excel de entrada requerido:** columnas según tipo de material.
  Descargar plantilla desde la app.

### 2. Ampliación sucursales
- Tipos de material: ZMED, ZNOM, ZINS
- Genera hojas: Datos básicos (almacenamiento), Datos de centro (~70 sucursales)
- El mapa de centros (WERKS → KOKRS / PRCTR) está en `config.py`

### 3. Modificación datos básicos
- Todos los tipos de material
- Genera hoja: Datos básicos (solo campos modificables)
- Campos modificables según tipo: MAKTX, PRDHA, VOLUM, TEXTO_LARGO, MSTAE

## Agregar o modificar tipos de material

Editar `config.py`:
- `TIPOS_MATERIAL`: valores fijos, vistas, cadenas, valoración
- `CENTROS_LOGISTICOS`: centros por tipo de material
- `CENTRO_BENEFICIO_MAP`: mapa de sucursales

## Notas

- El archivo generado es un `.xlsx`. Para subirlo a SAP hay que convertirlo
  a `.txt` con el proceso habitual.
- Los campos marcados con `-` en la configuración se generan vacíos.
- El campo MSTAE = `/` deja el material sin bloqueo; dejarlo vacío lo bloquea.
