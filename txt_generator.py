# =============================================================================
# txt_generator.py — Genera los archivos .txt con formato SAP
# Encoding: UTF-8, separador TAB, line endings CRLF, 2 filas de encabezado
# =============================================================================

from config import CENTRO_BENEFICIO_MAP, VISTA_NOMBRES


def _txt(header_nombres: list, header_tecnicos: list, filas: list[list]) -> bytes:
    """
    Construye el contenido del .txt con:
      Fila 1: nombres humanos (separados por TAB)
      Fila 2: campos técnicos SAP
      Fila 3+: datos
    Devuelve bytes UTF-8 con CRLF.
    """
    lines = []
    lines.append("\t".join(header_nombres))
    lines.append("\t".join(header_tecnicos))
    for fila in filas:
        lines.append("\t".join(str(v) if v is not None else "" for v in fila))
    return "\r\n".join(lines).encode("utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# DATOS BÁSICOS
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_basicos(materiales: list[dict], cfg: dict, vistas_key: str) -> bytes:
    """
    materiales: lista de dicts con campos del formulario
    cfg: dict del tipo de material desde TIPOS_MATERIAL
    vistas_key: "vistas_CL" | "vistas_SUC" | "vistas_MOD"
    """
    vistas_activas = cfg[vistas_key]

    TODAS_VISTAS = ["B","V","C","MRP","P","A","WM","CO","MRPAREA"]
    h_nombres = ["Número de producto"] + [VISTA_NOMBRES[v] for v in TODAS_VISTAS] + [
        "Clase de producto","Grupo de productos","Descripción","Código de idioma",
        "Partición","Jerarquía de productos","Indicador Gestión de lotes necesaria",
        "Grupo de clases de artículo general","Volumen","Unidad de volumen",
        "Clave de valor de compras","Grupo de transporte",
        "Indicador de periodo para caducidad","Caducidad residual mínima",
        "Perfil Serie","Texto largo","Bloqueo de material ",
    ]
    h_tecnicos = ["MATNR"] + [""]*9 + [
        "MTART","MATKL","MAKTX","SPRAS","SPART","PRDHA","XCHPF","MTPOS",
        "VOLUM","VOLEH","EKWSL","TRAGR","IPRKZ","MHDRZ","SERIAL","","MSTAE",
    ]

    filas = []
    for m in materiales:
        fila = [m["MATNR"]]
        for v in TODAS_VISTAS:
            fila.append("X" if v in vistas_activas else "")
        fila += [
            cfg.get("MTART",""),
            m.get("MATKL",""),
            m.get("MAKTX",""),
            "ES",
            m.get("SPART", cfg.get("SPART","")),
            m.get("PRDHA",""),
            cfg.get("XCHPF",""),
            cfg.get("MTPOS",""),
            m.get("VOLUM",""),
            cfg.get("VOLEH",""),
            cfg.get("EKWSL",""),
            cfg.get("TRAGR",""),
            cfg.get("IPRKZ",""),
            cfg.get("MHDRZ",""),
            cfg.get("SERIAL",""),
            m.get("TEXTO_LARGO", m.get("MAKTX","")),
            m.get("MSTAE",""),
        ]
        filas.append(fila)

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# DATOS DE CENTRO — centros logísticos
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_centro_CL(materiales: list[dict], cfg: dict) -> bytes:
    h_nombres = [
        "Número de producto","Centro","Tipo de MRP","Planificador de necesidades",
        "Verificación de disponibilidad","Sociedad CO","Centro de beneficio",
        "Indicador sol.gestión de lotes","Perfil Serie","Grupo de carga",
        "Grupo de compra","Pedido automático permitido","Indicador de impuestos",
        "Grupo MRP","Punto de reorganización","Cálculo de tamaño de lote",
        "Tamaño de lote mínimo","Tamaño de lote máximo","Tamaño de lote fijo",
        "Clase de aprovisionamiento","Almacén estándar p.aprovisionam.externo",
        "Hora de entrega planificada",
    ]
    h_tecnicos = [
        "MATNR","WERKS","DISMM","DISPO","MTVFP","KOKRS","PRCTR",
        "XCHPF","SERNP","LADGR","EKGRP","KAUTB","TAXIM","DISGR",
        "MINBE","DISLS","BSTMI","BSTMA","BSTFE","BESKZ","LGFSB","PLIFZ",
    ]

    filas = []
    for m in materiales:
        for centro in cfg["CL_centros"]:
            werks = centro["WERKS"]
            # EKGRP y TAXIM pueden ser por-material (el formulario los guarda con clave WERKS)
            ekgrp = m.get(f"EKGRP_{werks}", centro.get("EKGRP",""))
            taxim = m.get(f"TAXIM_{werks}", centro.get("TAXIM",""))
            fila = [
                m["MATNR"],
                werks,
                centro.get("DISMM",""),
                centro.get("DISPO",""),
                centro.get("MTVFP",""),
                centro.get("KOKRS",""),
                centro.get("PRCTR",""),
                centro.get("XCHPF",""),
                centro.get("SERNP",""),
                centro.get("LADGR",""),
                ekgrp,
                centro.get("KAUTB",""),
                taxim,
                centro.get("DISGR",""),
                centro.get("MINBE",""),
                centro.get("DISLS",""),
                centro.get("BSTMI",""),
                centro.get("BSTMA",""),
                centro.get("BSTFE",""),
                centro.get("BESKZ",""),
                centro.get("LGFSB",""),
                centro.get("PLIFZ",""),
            ]
            filas.append(fila)

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# DATOS DE CENTRO — sucursales
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_centro_SUC(materiales: list[dict], cfg: dict) -> bytes:
    h_nombres = [
        "Número de producto","Centro","Tipo de MRP","Planificador de necesidades",
        "Verificación de disponibilidad","Sociedad CO","Centro de beneficio",
        "Indicador sol.gestión de lotes","Perfil Serie","Grupo de carga",
        "Grupo de compra","Pedido automático permitido","Indicador de impuestos",
        "Grupo MRP","Punto de reorganización","Cálculo de tamaño de lote",
        "Tamaño de lote mínimo","Tamaño de lote máximo","Tamaño de lote fijo",
        "Clase de aprovisionamiento","Almacén estándar p.aprovisionam.externo",
        "Hora de entrega planificada",
    ]
    h_tecnicos = [
        "MATNR","WERKS","DISMM","DISPO","MTVFP","KOKRS","PRCTR",
        "XCHPF","SERNP","LADGR","EKGRP","KAUTB","TAXIM","DISGR",
        "MINBE","DISLS","BSTMI","BSTMA","BSTFE","BESKZ","LGFSB","PLIFZ",
    ]

    tiene_extra = cfg.get("SUC_datos_centro", False)

    filas = []
    for m in materiales:
        for werks, datos in CENTRO_BENEFICIO_MAP.items():
            fila = [
                m["MATNR"], werks, "", "", "",
                datos["KOKRS"], datos["PRCTR"],
                "", "", "",
                cfg.get("SUC_ekgrp","") if tiene_extra else "",
                cfg.get("SUC_kautb","") if tiene_extra else "",
                cfg.get("SUC_taxim","") if tiene_extra else "",
                "","","","","","","","","",
            ]
            filas.append(fila)

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# CADENAS DE DISTRIBUCIÓN
# ─────────────────────────────────────────────────────────────────────────────
def gen_cadenas(materiales: list[dict], cfg: dict) -> bytes | None:
    if not cfg.get("CL_cadenas"):
        return None

    h_nombres = [
        "Número de producto","Organización de ventas","Canal de distribución",
        "Centro suministrador","Grupo de categoría de posición",
        "Grupo de imputación","Jerarquía de productos",
    ]
    h_tecnicos = ["MATNR","VKORG","VTWEG","DWERK","MTPOS","KTGRM","PRODH"]

    filas = []
    for m in materiales:
        ktgrm = m.get("KTGRM", cfg.get("CL_ktgrm_opciones",[""])[0])
        for cadena in cfg["CL_cadenas"]:
            for canal in cadena["canales"]:
                filas.append([
                    m["MATNR"],
                    cadena["VKORG"],
                    canal,
                    cadena["DWERK"],
                    cadena["MTPOS"],
                    ktgrm,
                    m.get("PRDHA",""),
                ])

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# CLASIFICACIÓN FISCAL
# ─────────────────────────────────────────────────────────────────────────────
def gen_clasificacion_fiscal(materiales: list[dict], cfg: dict) -> bytes | None:
    if not cfg.get("CL_fiscal"):
        return None

    h_nombres = [
        "Número de producto","País/Región",
        "Clase de impuesto 1","Clasificación fiscal 1",
        "Clase de impuesto 2","Clasificación fiscal 2",
        "Clase de impuesto 3","Clasificación fiscal 3",
        "Clase de impuesto 4","Clasificación fiscal 4",
        "Clase de impuesto 5","Clasificación fiscal 5",
    ]
    h_tecnicos = [
        "MATNR","ALAND",
        "TATYP1","TAXM1","TATYP2","TAXM2",
        "TATYP3","TAXM3","TATYP4","TAXM4","TATYP5","TAXM5",
    ]

    filas = []
    for m in materiales:
        filas.append([
            m["MATNR"], "AR",
            "J1AU", cfg["CL_fiscal"]["TAXM1"],
            "J901", cfg["CL_fiscal"]["TAXM2"],
            "","","","","","",
        ])

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# DATOS DE PREVISIÓN
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_prevision(materiales: list[dict], cfg: dict) -> bytes | None:
    if not cfg.get("CL_prevision"):
        return None

    h_nombres = ["Número de producto","Centro","Modelo de pronóstico"]
    h_tecnicos = ["MATNR","WERKS","PRMOD"]

    filas = [[m["MATNR"], "A130", "J"] for m in materiales]
    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# LUGARES DE ALMACENAMIENTO
# ─────────────────────────────────────────────────────────────────────────────
def gen_lugares_almacenamiento(materiales: list[dict], cfg: dict) -> bytes | None:
    lugares = cfg.get("CL_lugares", {})
    if not lugares:
        return None

    h_nombres = ["Número de producto","Centro","Ubicación de almacén"]
    h_tecnicos = ["MATNR","WERKS","LGORT"]

    filas = []
    for m in materiales:
        for werks, ubicaciones in lugares.items():
            for lgort in ubicaciones:
                filas.append([m["MATNR"], werks, lgort])

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# ÁREA PLANIFICACIÓN MRP
# ─────────────────────────────────────────────────────────────────────────────
def gen_area_planificacion(materiales: list[dict], cfg: dict) -> bytes | None:
    if not cfg.get("CL_area_planif"):
        return None

    h_nombres = [
        "Número de producto","Centro","Área planif.MRP","Tipo de MRP",
        "Planificador de necesidades","Grupo MRP","Punto de reorganización",
        "Cálculo de tamaño de lote","Tamaño de lote mínimo","Tamaño de lote máximo",
        "Tamaño de lote fijo","Hora de entrega planificada",
        "Procedimiento de selección de modelo","Indicador de inicialización",
        "Modelo de pronóstico","Límite de alarma","Cantidad de períodos del pasado",
        "Cantidad de períodos de pronóstico","Anular automáticamente modelo pronóstico",
    ]
    h_tecnicos = [
        "MATNR","WERKS","BERID","DISMM","DISPO","DISGR","MINBE","DISLS",
        "BSTMI","BSTMA","BSTFE","PLIFZ","MODAV","KZINI","PRMOD","SIGGR",
        "PERAN","ANZPR","AUTRU",
    ]

    filas = []
    for m in materiales:
        filas.append([
            m["MATNR"], "A130", "A130_0040", "V1", "Z01",
            "0000", "10", "EX", "1", "", "", "4", "2", "X", "J", "4", "60", "12", "X",
        ])

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# DATOS DE VALORACIÓN
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_valoracion(materiales: list[dict], cfg: dict, clave: str = "CL_valoracion") -> bytes | None:
    val_cfg = cfg.get(clave, [])
    if not val_cfg:
        return None

    h_nombres = [
        "Número de producto","Área de valoración","Categoría de valoración",
        "Control de precios","Moneda","Media variable de precio de inventario",
        "Precio estándar de precio de inventario","Unidad de precio",
    ]
    h_tecnicos = ["MATNR","BWKEY","BKLAS","VPRSV","WAERS","VERPR","STPRS ","PEINH"]

    filas = []
    for m in materiales:
        for v in val_cfg:
            filas.append([
                m["MATNR"], v["BWKEY"], v["BKLAS"], v["VPRSV"],
                "ARS", v.get("VERPR",""), v.get("STPRS",""), v.get("PEINH","1"),
            ])

    return _txt(h_nombres, h_tecnicos, filas)


def gen_datos_valoracion_SUC(materiales: list[dict], cfg: dict) -> bytes | None:
    """Valoración para sucursales (ZINS): una fila por material × sucursal."""
    if not cfg.get("SUC_valoracion"):
        return None

    h_nombres = [
        "Número de producto","Área de valoración","Categoría de valoración",
        "Control de precios","Moneda","Media variable de precio de inventario",
        "Precio estándar de precio de inventario","Unidad de precio",
    ]
    h_tecnicos = ["MATNR","BWKEY","BKLAS","VPRSV","WAERS","VERPR","STPRS ","PEINH"]

    filas = []
    for m in materiales:
        for werks in CENTRO_BENEFICIO_MAP.keys():
            filas.append([
                m["MATNR"], werks,
                cfg["SUC_bklas"], cfg["SUC_vprsv"],
                "ARS", cfg["SUC_verpr"], "", cfg["SUC_peinh"],
            ])

    return _txt(h_nombres, h_tecnicos, filas)
