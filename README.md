# SAP — Ampliación masiva de materiales

Herramienta para generar los archivos `.txt` de carga masiva en SAP para los procesos de ampliación de centros logísticos, ampliación de sucursales y modificación de datos básicos de materiales.

---

## Requisitos

- Python 3.10 o superior
- Windows (la app corre en cualquier OS, pero está pensada para entornos Windows)

Para verificar si Python está instalado:

```powershell
python --version
```

Si no está instalado, descargarlo desde [python.org/downloads](https://www.python.org/downloads/). Durante la instalación, marcar la casilla **"Add Python to PATH"**.

---

## Instalación

Descomprimir el ZIP y desde la carpeta del proyecto instalar las dependencias:

```powershell
cd C:\sap_app
python -m pip install streamlit pandas
```

---

## Cómo correr la aplicación

```powershell
python -m streamlit run app.py
```

El navegador se abre automáticamente en `http://localhost:8501`. Si no se abre solo, pegá esa URL manualmente.

Para detener la aplicación presionár `Ctrl + C` en la terminal.

---

## Estructura del proyecto

```
sap_app/
├── app.py              Interfaz de usuario (Streamlit)
├── config.py           Configuración central: tipos de material, valores fijos, opciones de campos, mapa de centros
├── txt_generator.py    Generadores de cada vista (.txt)
└── requirements.txt    Dependencias
```

---

## Flujos disponibles

La app tiene tres flujos, seleccionables desde el panel izquierdo.

### 1. Ampliación centros logísticos

Genera los archivos necesarios para ampliar un material a los centros logísticos (A110, A120, A130 según el tipo).

**Tipos de material soportados:** ZMED, ZNOM, ZINS, ZSER\_C, ZSER\_NC, ZNOA, ZCOM

**Archivos que genera según tipo de material:**

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

**Campos que completa el usuario:**

| Campo | Descripción | Tipo |
|---|---|---|
| MATNR | Número de material | Texto libre |
| MAKTX | Descripción del material | Texto libre |
| MATKL | Grupo de productos | Texto libre |
| PRDHA | Jerarquía de productos | Texto libre |
| TEXTO\_LARGO | Texto largo | Texto libre |
| VOLUM | Volumen | Numérico (solo tipos con VOLEH) |
| SPART | Partición | Desplegable (solo ZNOM: S2 / S3) |
| EKGRP\_Axxx | Grupo de compra por centro | Desplegable |
| TAXIM\_Axxx | Indicador de impuestos por centro | Desplegable |
| KTGRM | Grupo de imputación | Desplegable |
| Bloquear material | Activa o desactiva el bloqueo | Checkbox |

---

### 2. Ampliación sucursales

Genera los archivos para ampliar un material a los ~70 centros de sucursales. El mapeo de cada centro a su sociedad CO y centro de beneficio está configurado en `config.py` y no requiere intervención del usuario.

**Tipos de material soportados:** ZMED, ZNOM, ZINS

**Archivos que genera:**

| Archivo | ZMED | ZNOM | ZINS |
|---|:---:|:---:|:---:|
| Datos\_basicos.txt | ✅ | ✅ | ✅ |
| Datos\_de\_centro.txt | ✅ | ✅ | ✅ |
| Datos\_valoracion.txt | — | — | ✅ |

**Campos que completa el usuario:** solo MATNR. El resto (sociedad CO, centro de beneficio, indicador de impuestos) se toma automáticamente del mapa de centros.

---

### 3. Modificación datos básicos

Genera el archivo `Datos_basicos.txt` para modificar campos de materiales existentes.

**Tipos de material soportados:** ZMED, ZNOM, ZINS, ZSER\_C, ZSER\_NC, ZNOA, ZCOM

**Campos modificables según tipo:**

| Campo | ZMED | ZNOM | ZINS | ZSER | ZNOA | ZCOM |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| MAKTX — Descripción | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PRDHA — Jerarquía | ✅ | ✅ | — | — | — | — |
| VOLUM — Volumen | ✅ | ✅ | — | — | — | — |
| TEXTO\_LARGO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MSTAE — Bloqueo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Formato de los archivos generados

Los `.txt` generados respetan exactamente el formato que SAP espera:

- **Separador:** tabulación (`TAB`)
- **Fila 1:** nombres de campo en español (ej. `Número de producto`)
- **Fila 2:** nombres técnicos SAP (ej. `MATNR`)
- **Fila 3 en adelante:** datos de los materiales
- **Encoding:** UTF-8
- **Fin de línea:** CRLF (Windows)

El resultado se descarga como un `.zip` que contiene un archivo `.txt` por cada vista generada. Para cargar en SAP, extraer el `.zip` y usar cada `.txt` individualmente con el proceso habitual de carga masiva.

---

## Cómo agregar o modificar tipos de material

Todo el comportamiento de la app se controla desde `config.py`. No hace falta tocar `app.py` ni `txt_generator.py` para ajustes de negocio.

**Para cambiar un valor fijo** (por ejemplo el PLIFZ de A130 para ZNOM):

```python
# En config.py, dentro de TIPOS_MATERIAL["ZNOM"]["CL_centros"]
{
    "WERKS": "A130",
    ...
    "PLIFZ": "5",   # ← cambiar acá
}
```

**Para agregar una opción a un desplegable** (por ejemplo un nuevo grupo de compra):

```python
# En config.py, sección OPCIONES
"EKGRP_ZMED_ZNOM": ["001", "002", "003", "004", "005", "008"],  # ← agregar "008"
```

**Para agregar un nuevo centro al mapa de sucursales:**

```python
# En config.py, en CENTRO_BENEFICIO_MAP
"0077": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
```

**Para agregar un nuevo tipo de material:** copiar una entrada existente de `TIPOS_MATERIAL` como base y ajustar los valores.

---

## Lógica del checkbox "Bloquear material"

El campo `MSTAE` en SAP funciona de forma contra-intuitiva:

| Checkbox en la app | Valor en el .txt | Efecto en SAP |
|---|---|---|
| ✅ Marcado | `/` | Material **activo** (sin bloqueo) |
| ☐ Desmarcado | *(vacío)* | Material **bloqueado** |

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| **Python 3.10+** | Lenguaje base |
| **Streamlit** | Interfaz web (formulario, tabla de materiales, descarga) |
| **pandas** | Manejo de timestamps para el nombre del ZIP |
| **zipfile** (stdlib) | Empaquetado de los `.txt` en un único ZIP descargable |
| **io.BytesIO** (stdlib) | Generación de archivos en memoria, sin escritura en disco |