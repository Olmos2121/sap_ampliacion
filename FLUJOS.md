# Flujo de operaciones por tipo de material

Documentación detallada de cada combinación de operación y tipo de material: qué vistas se generan, qué campos completa el usuario y qué valores son fijos del sistema.

---

## Índice

- [Cómo usar la aplicación](#cómo-usar-la-aplicación)
- [Operación 1 — Ampliación centros logísticos](#operación-1--ampliación-centros-logísticos)
  - [ZMED](#zmed--medicamentos)
  - [ZNOM](#znom--nomenclados)
  - [ZINS](#zins--insumos)
  - [ZSER\_C](#zser_c--servicios-con-compra-en-sucursales)
  - [ZSER\_NC](#zser_nc--servicios-sin-compra-en-sucursales)
  - [ZNOA](#znoa--no-almacenables)
  - [ZCOM](#zcom--componentes)
- [Operación 2 — Ampliación sucursales](#operación-2--ampliación-sucursales)
  - [ZMED (sucursales)](#zmed--sucursales)
  - [ZNOM (sucursales)](#znom--sucursales)
  - [ZINS (sucursales)](#zins--sucursales)
- [Operación 3 — Modificación datos básicos](#operación-3--modificación-datos-básicos)
- [Referencia rápida de campos](#referencia-rápida-de-campos)

---

## Cómo usar la aplicación

Toda operación sigue el mismo flujo de dos pasos antes de llegar al formulario:

**Paso 1 — Configurar operación**
1. Elegí el tipo de operación (centros logísticos / sucursales / modificación)
2. Elegí el tipo de material (ZMED, ZNOM, etc.)
3. Pegá los números de material (MATNR) desde Excel — una columna, un número por línea

**Paso 2 — Completar vistas**
- Cada pestaña corresponde a una vista de SAP y a un `.txt` de salida
- Podés navegar libremente entre pestañas; los datos se conservan
- Las tablas muestran una fila por material. El botón **"↕ Aplicar a todos"** copia el valor del primero a todos los demás
- El botón **"⚙️ Generar .txt"** está en cada pestaña y genera todos los archivos del flujo

**Descarga**
- Se descarga un ZIP con un `.txt` por cada vista que aplica al tipo de material

---

## Operación 1 — Ampliación centros logísticos

Amplía un material nuevo a los centros logísticos (A110, A120, A130 según el tipo). Solo aplica a materiales que **no existen aún** en esos centros.

---

### ZMED — Medicamentos

**Centros:** A130 + A110

**Archivos generados:** 8

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |
| Cadenas de distribución | `Cadenas_de_distribucion.txt` |
| Clasificación fiscal | `Clasificacion_fiscal.txt` |
| Datos de previsión | `Datos_de_prevision.txt` |
| Lugares de almacenamiento | `Lugares_de_almacenamiento.txt` |
| Área planif. MRP | `Area_planific_nec.txt` |
| Datos de valoración | `Datos_valoracion.txt` |

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Volumen | VOLUM | Número (en CM3) |
| Texto largo | TEXTO\_LARGO | Texto libre (default: descripción) |
| Estado del material | MSTAE | Checkbox — ✅ activo `/` / ☐ bloqueado |
| Grupo de compra A130 | EKGRP | Desplegable: 001, 002, 003, 004, 005 |
| Grupo de compra A110 | EKGRP | Desplegable: 001, 002, 003, 004, 005 |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1 – 7 |
| Indicador de impuestos A110 | TAXIM | Desplegable: 1 – 7 |
| Grupo de imputación | KTGRM | Desplegable: 01, 02 |

**Valores fijos del sistema:**

| Campo | Valor |
|-------|-------|
| MTART | ZMED |
| SPART | S1 |
| XCHPF | X (gestión de lotes) |
| MTPOS | NORM |
| VOLEH | CM3 |
| EKWSL | 1 |
| TRAGR | 0001 |
| IPRKZ | D (caducidad) |
| MHDRZ | 270 días |
| SERIAL | TRAZ |

**Datos de centro — valores fijos por centro:**

| Campo | A130 | A110 |
|---|---|---|
| KOKRS | AR01 | AR01 |
| PRCTR | AR01021400 | AR01031200 |
| DISMM | V1 | — |
| DISPO | Z01 | — |
| MTVFP | 02 | 02 |
| LADGR | 0001 | 0001 |
| KAUTB | X | X |
| DISGR | 0000 | — |
| MINBE | 10 | — |
| DISLS | EX | — |
| BSTMI | 1 | — |
| BESKZ | F | — |
| LGFSB | 0040 | — |
| PLIFZ | 4 | — |
| XCHPF | — | X |
| SERNP | — | TRAZ |

**Cadenas de distribución:**

| VKORG | Canales | Centro suministrador | MTPOS | KTGRM |
|---|---|---|---|---|
| 3001 | 30, 40, 50 | A130 | NORM | el que ingresó el usuario |
| 1001 | 10, 20, 30, 40, 50 | A110 | NORM | el que ingresó el usuario |

**Clasificación fiscal:** TAXM1 = 0, TAXM2 = 0

**Datos de previsión:** Centro A130, PRMOD = J

**Lugares de almacenamiento:**

| Centro | Ubicaciones |
|---|---|
| A130 | 0040, 0041, 0042, 0043 |
| A110 | 0010, 0011, 0020, 0021, 0022 |

**Datos de valoración:**

| Centro | BKLAS | VPRSV | Precio |
|---|---|---|---|
| A130 | 3101 | V (variable) | VERPR = 20 |
| A110 | 3101 | V (variable) | VERPR = 200 |

---

### ZNOM — Nomenclados

**Centros:** A130 + A120

**Archivos generados:** 8 (igual a ZMED)

**Diferencias respecto a ZMED:**
- No tiene gestión de lotes (XCHPF) ni perfil serie (SERIAL/SERNP)
- No tiene caducidad (IPRKZ / MHDRZ)
- SPART: desplegable S2 / S3 (el usuario elige)
- Segundo centro es A120 en lugar de A110
- BKLAS = 3300 (en lugar de 3101)
- KTGRM: solo opción 03

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Volumen | VOLUM | Número (en CM3) |
| Partición | SPART | Desplegable: S2, S3 |
| Texto largo | TEXTO\_LARGO | Texto libre |
| Estado del material | MSTAE | Checkbox |
| Grupo de compra A130 | EKGRP | Desplegable: 001–005 |
| Grupo de compra A120 | EKGRP | Desplegable: 001–005 |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1–7 |
| Indicador de impuestos A120 | TAXIM | Desplegable: 1–7 |
| Grupo de imputación | KTGRM | Fijo: 03 |

**Datos de valoración:**

| Centro | BKLAS | VPRSV | Precio |
|---|---|---|---|
| A130 | 3300 | V | VERPR = 20 |
| A120 | 3300 | V | VERPR = 200 |

**Lugares de almacenamiento:**

| Centro | Ubicaciones |
|---|---|
| A130 | 0040, 0041, 0042, 0043 |
| A120 | 0030, 0031 |

---

### ZINS — Insumos

**Centros:** A130 + A120

**Archivos generados:** 6 (sin previsión ni área MRP)

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |
| Cadenas de distribución | `Cadenas_de_distribucion.txt` |
| Clasificación fiscal | `Clasificacion_fiscal.txt` |
| Lugares de almacenamiento | `Lugares_de_almacenamiento.txt` |
| Datos de valoración | `Datos_valoracion.txt` |

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Volumen | VOLUM | Número (en CM3) |
| Texto largo | TEXTO\_LARGO | Texto libre |
| Estado del material | MSTAE | Checkbox |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1–7 |
| Indicador de impuestos A120 | TAXIM | Desplegable: 1–7 |

**Valores fijos destacados:**

| Campo | Valor |
|---|---|
| EKGRP | 007 (fijo, no editable) |
| MTVFP | 02 |
| KAUTB | X |
| SPART | S2 |
| MTPOS | NORM |
| TAXM1 (fiscal) | 1 |

**Datos de valoración:**

| Centro | BKLAS | VPRSV | Precio |
|---|---|---|---|
| A130 | 3400 | V | VERPR = 0.04 |
| A120 | 3400 | V | VERPR = 0.04 |

**Lugares de almacenamiento:**

| Centro | Ubicaciones |
|---|---|
| A130 | 0040, 0041, 0042, 0043 |
| A120 | 0030, 0031 |

---

### ZSER\_C — Servicios con compra en sucursales

**Centros:** A130 + A110

**Archivos generados:** 5 (sin previsión, área MRP ni lugares)

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |
| Cadenas de distribución | `Cadenas_de_distribucion.txt` |
| Clasificación fiscal | `Clasificacion_fiscal.txt` |
| Datos de valoración | `Datos_valoracion.txt` |

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Texto largo | TEXTO\_LARGO | Texto libre |
| Estado del material | MSTAE | Checkbox |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1–7 |
| Indicador de impuestos A110 | TAXIM | Desplegable: 1–7 |
| Grupo de imputación | KTGRM | Desplegable: 04, 05 |

> ZSER\_C no tiene campo Volumen.

**Valores fijos destacados:**

| Campo | Valor |
|---|---|
| SPART | S4 |
| MTPOS | LEIS |
| EKWSL | 1 |
| EKGRP | 006 (fijo) |
| MTVFP | KP |
| KAUTB | X |
| TAXM1 (fiscal) | 1 |

**Diferencia con ZSER\_NC:** ZSER\_C activa la vista de Compras (C) y tiene EKGRP y MTVFP configurados. ZSER\_NC no activa esa vista.

**Datos de valoración:**

| Centro | BKLAS | VPRSV | Precio |
|---|---|---|---|
| A130 | 3233 | S (estándar) | STPRS = 4 |
| A110 | 3233 | S (estándar) | STPRS = 4 |

---

### ZSER\_NC — Servicios sin compra en sucursales

**Centros:** A130 + A110

**Archivos generados:** 5 (igual a ZSER\_C)

**Diferencias respecto a ZSER\_C:**
- No activa la vista de Compras (C)
- No tiene EKGRP configurable ni MTVFP
- En Datos de centro solo se registra TAXIM y los datos de sociedad CO / beneficio

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Texto largo | TEXTO\_LARGO | Texto libre |
| Estado del material | MSTAE | Checkbox |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1–7 |
| Indicador de impuestos A110 | TAXIM | Desplegable: 1–7 |
| Grupo de imputación | KTGRM | Desplegable: 04, 05 |

**Datos de valoración:** igual a ZSER\_C (BKLAS 3233, VPRSV S, STPRS 4)

---

### ZNOA — No almacenables

**Centros:** A110 + A120 + A130 (los tres centros logísticos)

**Archivos generados:** 3 (sin cadenas, fiscal ni lugares)

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |
| Datos de valoración | `Datos_valoracion.txt` |

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Texto largo | TEXTO\_LARGO | Texto libre |
| Estado del material | MSTAE | Checkbox |
| Indicador de impuestos A110 | TAXIM | Desplegable: 1–7 |
| Indicador de impuestos A120 | TAXIM | Desplegable: 1–7 |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1–7 |

> ZNOA no tiene partición (SPART), grupo de transporte (TRAGR), clave de valor de compras (EKWSL) ni cadenas de distribución.

**Valores fijos destacados:**

| Campo | Valor |
|---|---|
| MTPOS | NLAG (no almacenable) |
| KAUTB | X |
| EKGRP | 006 (fijo en los tres centros) |

**Datos de valoración:**

| Centro | BKLAS | VPRSV | Precio |
|---|---|---|---|
| A110 | 3507 | V | VERPR = 1 |
| A120 | 3507 | V | VERPR = 1 |
| A130 | 3507 | V | VERPR = 1 |

---

### ZCOM — Componentes

**Centros:** A130 únicamente

**Archivos generados:** 5 (sin previsión, área MRP, lugares de almacenamiento ni valoración)

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |
| Cadenas de distribución | `Cadenas_de_distribucion.txt` |
| Clasificación fiscal | `Clasificacion_fiscal.txt` |
| Lugares de almacenamiento | `Lugares_de_almacenamiento.txt` |

**Campos que completa el usuario:**

| Campo | Técnico | Tipo |
|---|---|---|
| Descripción | MAKTX | Texto libre |
| Grupo de productos | MATKL | Texto libre |
| Jerarquía de productos | PRDHA | Texto libre |
| Volumen | VOLUM | Número (en CM3) |
| Texto largo | TEXTO\_LARGO | Texto libre |
| Estado del material | MSTAE | Checkbox |
| Indicador de impuestos A130 | TAXIM | Desplegable: 1–7 |
| Grupo de imputación | KTGRM | Fijo: 03 |

**Valores fijos destacados:**

| Campo | Valor |
|---|---|
| SPART | S2 |
| MTPOS | ERLA (componente) |
| TRAGR | 0001 |
| MTVFP | KP |
| LADGR | 0001 |
| KOKRS | AR01 |
| PRCTR | AR01021400 |
| TAXM1 (fiscal) | 1 |

**Cadenas de distribución:** solo organización 3001, canales 30 / 40 / 50, centro suministrador A130.

**Lugares de almacenamiento:** A130 → 0040, 0041, 0042, 0043

> ZCOM no genera datos de valoración.

---

## Operación 2 — Ampliación sucursales

Amplía un material a los **70 centros de sucursales**. Para cada material se genera una fila por cada sucursal del mapa configurado en `config.py`. El usuario solo ingresa los MATNR; el resto se toma del mapa automáticamente.

Solo disponible para ZMED, ZNOM y ZINS.

---

### ZMED — Sucursales

**Archivos generados:** 2

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |

**Campos que completa el usuario:** solo MATNR (pegado en el paso 1).

**Datos básicos:** activa únicamente la vista de almacenamiento (A). No requiere descripción, jerarquía ni volumen.

**Datos de centro:** se genera una fila por sucursal con KOKRS y PRCTR del mapa. No se generan campos adicionales (EKGRP, TAXIM, etc.) para ZMED en sucursales.

---

### ZNOM — Sucursales

**Archivos generados:** 2 (igual a ZMED sucursales)

Mismo comportamiento que ZMED. Activa solo vista de almacenamiento, sin campos adicionales en datos de centro.

---

### ZINS — Sucursales

**Archivos generados:** 3

| Vista | Archivo generado |
|---|---|
| Datos básicos | `Datos_basicos.txt` |
| Datos de centro | `Datos_de_centro.txt` |
| Datos de valoración | `Datos_valoracion.txt` |

**Campos que completa el usuario:** solo MATNR.

**Diferencias respecto a ZMED/ZNOM en sucursales:**
- Activa además la vista de Contabilidad (CO) en datos básicos
- Datos de centro incluye campos adicionales fijos: EKGRP = 007, KAUTB = X, TAXIM = 1
- Genera datos de valoración: BKLAS 3400, VPRSV V, VERPR 0.04 — una fila por material por cada sucursal (70 filas × cantidad de materiales)

---

## Operación 3 — Modificación datos básicos

Modifica campos de materiales **ya existentes** en SAP. Genera un único archivo `Datos_basicos.txt` con solo los campos que pueden cambiarse.

Disponible para todos los tipos de material.

**Campos modificables según tipo:**

| Campo | Técnico | ZMED | ZNOM | ZINS | ZSER\_C | ZSER\_NC | ZNOA | ZCOM |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Descripción | MAKTX | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Jerarquía de productos | PRDHA | ✅ | ✅ | — | — | — | — | — |
| Volumen | VOLUM | ✅ | ✅ | — | — | — | — | — |
| Texto largo | TEXTO\_LARGO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Estado (bloqueo) | MSTAE | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Vistas activas en el archivo generado:**

| Tipo | Vistas con X |
|---|---|
| ZMED | Datos básicos (B) + Compras (C) |
| ZNOM | Datos básicos (B) + Compras (C) |
| ZINS | Solo Datos básicos (B) |
| ZSER\_C | Solo Datos básicos (B) |
| ZSER\_NC | Solo Datos básicos (B) |
| ZNOA | Solo Datos básicos (B) |
| ZCOM | Solo Datos básicos (B) |

---

## Referencia rápida de campos

### Checkbox MSTAE — Estado del material

| Estado en la app | Valor en el .txt | Efecto en SAP |
|---|---|---|
| ✅ Marcado | `/` | Material **activo** (sin bloqueo) |
| ☐ Desmarcado | *(vacío)* | Material **bloqueado** |

### Centros logísticos por tipo

| Tipo | Centro 1 | Centro 2 | Centro 3 |
|---|---|---|---|
| ZMED | A130 | A110 | — |
| ZNOM | A130 | A120 | — |
| ZINS | A130 | A120 | — |
| ZSER\_C | A130 | A110 | — |
| ZSER\_NC | A130 | A110 | — |
| ZNOA | A110 | A120 | A130 |
| ZCOM | A130 | — | — |

### Categoría de valoración (BKLAS) por tipo

| Tipo | BKLAS | Control precio | Campo precio |
|---|---|---|---|
| ZMED | 3101 | V (variable) | VERPR |
| ZNOM | 3300 | V (variable) | VERPR |
| ZINS | 3400 | V (variable) | VERPR |
| ZSER\_C | 3233 | S (estándar) | STPRS |
| ZSER\_NC | 3233 | S (estándar) | STPRS |
| ZNOA | 3507 | V (variable) | VERPR |
| ZCOM | — | — | — |

### Grupo de imputación (KTGRM) disponible por tipo

| Tipo | Opciones |
|---|---|
| ZMED | 01, 02 |
| ZNOM | 03 |
| ZINS | 03 |
| ZSER\_C | 04, 05 |
| ZSER\_NC | 04, 05 |
| ZNOA | — (sin cadenas) |
| ZCOM | 03 |

### Vistas activas por tipo y operación

| Tipo | CL — vistas con X | Sucursales | Modificación |
|---|---|---|---|
| ZMED | B V C MRP P A WM CO MRPAREA | A | B C |
| ZNOM | B V C MRP P A WM CO MRPAREA | A | B C |
| ZINS | B V C A CO | A CO | B |
| ZSER\_C | B V C CO | — | B |
| ZSER\_NC | B V CO | — | B |
| ZNOA | B C CO | — | B |
| ZCOM | B V A | — | B |

> **Referencias:** B=Datos básicos, V=Ventas, C=Compras, MRP=MRP, P=Pronóstico, A=Almacenamiento, WM=WM, CO=Contabilidad, MRPAREA=Área MRP