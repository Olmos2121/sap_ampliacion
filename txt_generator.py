# =============================================================================
# txt_generator.py — Genera los archivos .txt con formato SAP
# Encoding: UTF-8, separador TAB, line endings CRLF, 2 filas de encabezado
# =============================================================================

from config import CENTRO_BENEFICIO_MAP, VISTA_NOMBRES


def _txt(header_nombres: list, header_tecnicos: list, filas: list[list]) -> bytes:
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

    es_sucursales = vistas_key == "vistas_SUC"
    es_modificacion = vistas_key == "vistas_MOD"

    filas = []
    for m in materiales:
        fila = [m["MATNR"]]
        for v in TODAS_VISTAS:
            fila.append("X" if v in vistas_activas else "")
        if es_sucursales:
            fila += [""] * 17
        elif es_modificacion:
            mod_campos = cfg.get("MOD_campos", [])
            volum_valor = m.get("VOLUM", "") if "VOLUM" in mod_campos else ""
            voleh_valor = cfg.get("VOLEH", "") if volum_valor else ""
            fila += [
                "",
                "",
                m.get("MAKTX","") if "MAKTX" in mod_campos else "",
                "ES" if "MAKTX" in mod_campos else "",
                "",
                m.get("PRDHA","") if "PRDHA" in mod_campos else "",
                "",
                "",
                volum_valor,
                voleh_valor,
                "",
                "",
                "",
                "",
                "",
                m.get("TEXTO_LARGO", m.get("MAKTX","")),
                m.get("MSTAE",""),
            ]
        else:
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
                m.get("SERIAL", cfg.get("SERIAL","")),
                m.get("TEXTO_LARGO", m.get("MAKTX","")),
                m.get("MSTAE",""),
            ]
        filas.append(fila)

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# DATOS DE CENTRO — centros logísticos
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_centro_CL(materiales: list[dict], cfg: dict, centros: list = None) -> bytes:
    centros = centros or [c["WERKS"] for c in cfg.get("CL_centros", [])]
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
        for centro in [c for c in cfg["CL_centros"] if centros is None or c["WERKS"] in centros]:
            werks = centro["WERKS"]
            ekgrp = m.get(f"EKGRP_{werks}", centro.get("EKGRP",""))
            taxim = m.get(f"TAXIM_{werks}", centro.get("TAXIM",""))
            sernp_cfg = centro.get("SERNP","")
            sernp = m.get("SERIAL", sernp_cfg) if sernp_cfg else ""
            fila = [
                m["MATNR"], werks,
                centro.get("DISMM",""), centro.get("DISPO",""), centro.get("MTVFP",""),
                centro.get("KOKRS",""), centro.get("PRCTR",""),
                centro.get("XCHPF",""), sernp, centro.get("LADGR",""),
                ekgrp, centro.get("KAUTB",""), taxim,
                centro.get("DISGR",""), centro.get("MINBE",""), centro.get("DISLS",""),
                centro.get("BSTMI",""), centro.get("BSTMA",""), centro.get("BSTFE",""),
                centro.get("BESKZ",""), centro.get("LGFSB",""), centro.get("PLIFZ",""),
            ]
            filas.append(fila)

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# DATOS DE CENTRO — sucursales
# ─────────────────────────────────────────────────────────────────────────────
def gen_datos_centro_SUC(materiales: list[dict], cfg: dict, mapa: dict = None) -> bytes:
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
    mapa_centros = mapa if mapa is not None else CENTRO_BENEFICIO_MAP

    filas = []
    for m in materiales:
        for werks, datos in mapa_centros.items():
            fila = [
                m["MATNR"], werks,
                "", "",
                cfg.get("SUC_mtvfp", "") if tiene_extra else "",
                datos["KOKRS"], datos["PRCTR"],
                "", "", "",
                cfg.get("SUC_ekgrp", "") if tiene_extra else "",
                cfg.get("SUC_kautb", "") if tiene_extra else "",
                cfg.get("SUC_taxim", "") if tiene_extra else "",
                "","","","","","","","","",
            ]
            filas.append(fila)

    return _txt(h_nombres, h_tecnicos, filas)


def gen_datos_centro_ZNOA(materiales: list[dict], cfg: dict, centros_cl: list = None) -> bytes:
    from config import CENTRO_BENEFICIO_MAP

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

    ekgrp = cfg.get("SUC_ekgrp", "006")
    kautb = cfg.get("SUC_kautb", "X")

    filas = []
    for m in materiales:
        taxim = m.get("TAXIM_SUC_znoa", "1")
        centros_a_usar = [c["WERKS"] for c in cfg.get("CL_centros", [])
                          if centros_cl is None or c["WERKS"] in centros_cl]
        for werks in centros_a_usar:
            filas.append([
                m["MATNR"], werks, "","","","","",
                "","", "",
                ekgrp, kautb, taxim,
                "","","","","","","","","",
            ])
        for werks in CENTRO_BENEFICIO_MAP.keys():
            filas.append([
                m["MATNR"], werks, "","","","","",
                "","","",
                ekgrp, kautb, taxim,
                "","","","","","","","","",
            ])

    return _txt(h_nombres, h_tecnicos, filas)


# ─────────────────────────────────────────────────────────────────────────────
# CADENAS DE DISTRIBUCIÓN
# ─────────────────────────────────────────────────────────────────────────────
def gen_cadenas(materiales: list[dict], cfg: dict, centros: list = None) -> bytes | None:
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
        for cadena in [c for c in cfg["CL_cadenas"] if centros is None or c["DWERK"] in centros]:
            for canal in cadena["canales"]:
                filas.append([
                    m["MATNR"], cadena["VKORG"], canal,
                    cadena["DWERK"], cadena["MTPOS"], ktgrm, m.get("PRDHA",""),
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
def gen_lugares_almacenamiento(materiales: list[dict], cfg: dict, centros: list = None) -> bytes | None:
    lugares = cfg.get("CL_lugares", {})
    if not lugares:
        return None

    h_nombres = ["Número de producto","Centro","Ubicación de almacén"]
    h_tecnicos = ["MATNR","WERKS","LGORT"]

    filas = []
    for m in materiales:
        for werks, ubicaciones in lugares.items():
            if centros is not None and werks not in centros:
                continue
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
def gen_datos_valoracion(materiales: list[dict], cfg: dict, clave: str = "CL_valoracion", centros: list = None) -> bytes | None:
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
        for v in [x for x in val_cfg if centros is None or x["BWKEY"] in centros]:
            filas.append([
                m["MATNR"], v["BWKEY"], v["BKLAS"], v["VPRSV"],
                "ARS", v.get("VERPR",""), v.get("STPRS",""), v.get("PEINH","1"),
            ])

    return _txt(h_nombres, h_tecnicos, filas)


def gen_datos_valoracion_ZNOA(materiales: list[dict], cfg: dict, centros_cl: list = None) -> bytes:
    from config import CENTRO_BENEFICIO_MAP

    h_nombres = [
        "Número de producto","Área de valoración","Categoría de valoración",
        "Control de precios","Moneda","Media variable de precio de inventario",
        "Precio estándar de precio de inventario","Unidad de precio",
    ]
    h_tecnicos = ["MATNR","BWKEY","BKLAS","VPRSV","WAERS","VERPR","STPRS ","PEINH"]

    val_cl = [v for v in cfg.get("CL_valoracion",[])
              if centros_cl is None or v["BWKEY"] in centros_cl]

    filas = []
    for m in materiales:
        for v in val_cl:
            filas.append([
                m["MATNR"], v["BWKEY"], v["BKLAS"], v["VPRSV"],
                "ARS", v.get("VERPR",""), v.get("STPRS",""), v.get("PEINH","1"),
            ])
        for werks in CENTRO_BENEFICIO_MAP.keys():
            filas.append([
                m["MATNR"], werks,
                cfg.get("SUC_bklas",""), cfg.get("SUC_vprsv",""),
                "ARS", cfg.get("SUC_verpr",""), "", cfg.get("SUC_peinh","1"),
            ])

    return _txt(h_nombres, h_tecnicos, filas)


def gen_datos_valoracion_SUC(materiales: list[dict], cfg: dict, mapa: dict = None) -> bytes | None:
    if not cfg.get("SUC_valoracion"):
        return None

    h_nombres = [
        "Número de producto","Área de valoración","Categoría de valoración",
        "Control de precios","Moneda","Media variable de precio de inventario",
        "Precio estándar de precio de inventario","Unidad de precio",
    ]
    h_tecnicos = ["MATNR","BWKEY","BKLAS","VPRSV","WAERS","VERPR","STPRS ","PEINH"]

    mapa_centros = mapa if mapa is not None else CENTRO_BENEFICIO_MAP

    filas = []
    for m in materiales:
        for werks in mapa_centros.keys():
            filas.append([
                m["MATNR"], werks,
                cfg["SUC_bklas"], cfg["SUC_vprsv"],
                "ARS",
                cfg.get("SUC_verpr", ""),
                cfg.get("SUC_stprs", ""),
                cfg["SUC_peinh"],
            ])

    return _txt(h_nombres, h_tecnicos, filas)