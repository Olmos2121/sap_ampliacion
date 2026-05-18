# ─────────────────────────────────────────────────────────────────────────────
# config.py — Configuración central de tipos de material y valores fijos
# Fuente: Datos_ampliacion_masiva_centros_logisticos.xlsx
# ─────────────────────────────────────────────────────────────────────────────

# Centros logísticos principales (para ampliación CL)
CENTROS_LOGISTICOS = {
    "ZMED": [
        {"WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400"},
        {"WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200"},
    ],
    "ZNOM": [
        {"WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400"},
        {"WERKS": "A120", "KOKRS": "AR01", "PRCTR": "AR01031200"},
    ],
    "ZINS": [
        {"WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400"},
        {"WERKS": "A120", "KOKRS": "AR01", "PRCTR": "AR01031200"},
    ],
    "ZSER_C": [
        {"WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400"},
        {"WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200"},
    ],
    "ZSER_NC": [
        {"WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400"},
        {"WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200"},
    ],
    "ZCOM": [
        {"WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400"},
    ],
}

# Mapa de sucursales: centro → sociedad CO + centro de beneficio
# Fuente: Ampliacion_sucursales.xlsx (los ~70 centros)
CENTRO_BENEFICIO_MAP = {
    "0002": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0004": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0005": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0006": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0007": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0008": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0009": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0010": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0011": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0012": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0013": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0014": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0015": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0016": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0017": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0018": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0019": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0020": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0021": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0022": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0023": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0024": {"KOKRS": "AR03", "PRCTR": "AR03011100"},
    "0025": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0026": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0027": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0028": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0029": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0030": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0031": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0032": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0034": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0035": {"KOKRS": "AR01", "PRCTR": "AR01011100"},
    "0036": {"KOKRS": "AR05", "PRCTR": "AR05011100"},
    "0037": {"KOKRS": "AR01", "PRCTR": "AR01011100"},
    "0038": {"KOKRS": "AR01", "PRCTR": "AR01011500"},
    "0039": {"KOKRS": "AR01", "PRCTR": "AR01011500"},
    "0040": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0042": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0043": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0044": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0045": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0046": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0047": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0048": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0049": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0050": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0051": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0052": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0053": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0054": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0055": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0056": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0058": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0059": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0060": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0061": {"KOKRS": "AR06", "PRCTR": "AR06011600"},
    "0062": {"KOKRS": "AR02", "PRCTR": "AR02011600"},
    "0063": {"KOKRS": "AR02", "PRCTR": "AR02011600"},
    "0064": {"KOKRS": "AR02", "PRCTR": "AR02011600"},
    "0065": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
    "0067": {"KOKRS": "AR06", "PRCTR": "AR06011600"},
    "0068": {"KOKRS": "AR06", "PRCTR": "AR06011600"},
    "0069": {"KOKRS": "AR02", "PRCTR": "AR02011600"},
    "0070": {"KOKRS": "AR02", "PRCTR": "AR02011600"},
    "0071": {"KOKRS": "AR03", "PRCTR": "AR03011600"},
    "0072": {"KOKRS": "AR06", "PRCTR": "AR06011600"},
    "0073": {"KOKRS": "AR07", "PRCTR": "AR07011100"},
    "0074": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0075": {"KOKRS": "AR04", "PRCTR": "AR04011100"},
    "0076": {"KOKRS": "AR02", "PRCTR": "AR02011100"},
}
SOCIEDAD_MAP = CENTRO_BENEFICIO_MAP  # alias


# ─────────────────────────────────────────────────────────────────────────────
# Configuración por tipo de material
# Cada entrada define:
#   - valores_fijos: dict campo→valor para datos básicos y centro
#   - vistas_activas: qué columnas "Vista de X" se marcan con X
#   - cadenas: configuración de org. de ventas / canales
#   - valoracion: categoría, control de precio, campo precio y valor
#   - campos_entrada: columnas que el usuario debe traer en su Excel
#   - campos_modificacion: columnas para el flujo de modificación
# ─────────────────────────────────────────────────────────────────────────────

TIPOS_MATERIAL = {
    "ZMED": {
        "vistas_basicos": ["B", "V", "C", "MRP", "P", "A", "WM", "CO"],
        "valores_fijos_basicos": {
            "MTART": "ZMED",
            "SPRAS": "ES",
            "SPART": "S1",
            "XCHPF": "X",
            "MTPOS": "NORM",
            "VOLEH": "CM3",
            "EKWSL": "1",
            "TRAGR": "0001",
            "IPRKZ": "D",
            "MHDRZ": "270",
            "SERIAL": "TRAZ",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {
            "DISMM": "V1", "DISPO": "Z01", "MTVFP": "02",
            "LADGR": "0001", "EKGRP": "001", "KAUTB": "X",
            "TAXIM": "6", "DISGR": "0000", "MINBE": "10",
            "DISLS": "EX", "BSTMI": "1", "BESKZ": "F",
            "LGFSB": "0040", "PLIFZ": "4",
        },
        "valores_fijos_centro_A110": {
            "MTVFP": "02", "LADGR": "0001", "EKGRP": "001",
            "KAUTB": "X", "TAXIM": "6", "XCHPF": "X", "SERNP": "TRAZ",
        },
        "cadenas": {
            "org_3001": {"canales": ["30", "40", "50"], "centro": "A130", "MTPOS": "NORM", "KTGRM": "01"},
            "org_1001": {"canales": ["10", "20", "30", "40", "50"], "centro": "A110", "MTPOS": "NORM", "KTGRM": "01"},
        },
        "fiscal": {"TAXM1": "0", "TAXM2": "0"},
        "prevision": True,
        "lugares_almacenamiento": {
            "A130": ["0040", "0041", "0042", "0043"],
            "A110": ["0010", "0011", "0020", "0021", "0022"],
        },
        "area_planificacion": True,
        "valoracion": [
            {"BWKEY": "A130", "BKLAS": "3101", "VPRSV": "V", "VERPR": "20", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3101", "VPRSV": "V", "VERPR": "200", "STPRS": "", "PEINH": "1"},
        ],
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "VOLUM", "EKGRP_A130", "EKGRP_A110", "TAXIM", "KTGRM"],
        "campos_modificacion": ["MATNR", "MAKTX", "PRDHA", "VOLUM", "TEXTO_LARGO", "MSTAE"],
    },

    "ZNOM": {
        "vistas_basicos": ["B", "V", "C", "MRP", "P", "A", "WM", "CO"],
        "valores_fijos_basicos": {
            "MTART": "ZNOM",
            "SPRAS": "ES",
            "SPART": "S2",
            "MTPOS": "NORM",
            "VOLEH": "CM3",
            "EKWSL": "1",
            "TRAGR": "0001",
            "IPRKZ": "D",
            "MHDRZ": "270",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {
            "DISMM": "V1", "DISPO": "Z01", "MTVFP": "02",
            "LADGR": "0001", "EKGRP": "001", "KAUTB": "X",
            "TAXIM": "6", "DISGR": "0000", "MINBE": "10",
            "DISLS": "EX", "BSTMI": "1", "BESKZ": "F",
            "LGFSB": "0040", "PLIFZ": "4",
        },
        "valores_fijos_centro_A120": {
            "MTVFP": "02", "LADGR": "0001", "EKGRP": "001",
            "KAUTB": "X", "TAXIM": "6",
        },
        "cadenas": {
            "org_3001": {"canales": ["30", "40", "50"], "centro": "A130", "MTPOS": "NORM", "KTGRM": "03"},
            "org_1001": {"canales": ["10", "20", "30", "40", "50"], "centro": "A120", "MTPOS": "NORM", "KTGRM": "03"},
        },
        "fiscal": {"TAXM1": "0", "TAXM2": "0"},
        "prevision": True,
        "lugares_almacenamiento": {
            "A130": ["0040", "0041", "0042", "0043"],
            "A120": ["0030", "0031"],
        },
        "area_planificacion": True,
        "valoracion": [
            {"BWKEY": "A130", "BKLAS": "3300", "VPRSV": "V", "VERPR": "20", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A120", "BKLAS": "3300", "VPRSV": "V", "VERPR": "200", "STPRS": "", "PEINH": "1"},
        ],
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "VOLUM", "EKGRP_A130", "TAXIM", "KTGRM"],
        "campos_modificacion": ["MATNR", "MAKTX", "PRDHA", "VOLUM", "TEXTO_LARGO", "MSTAE"],
    },

    "ZINS": {
        "vistas_basicos": ["B", "V", "C", "A", "CO"],
        "valores_fijos_basicos": {
            "MTART": "ZINS",
            "SPRAS": "ES",
            "SPART": "S2",
            "MTPOS": "NORM",
            "VOLEH": "CM3",
            "EKWSL": "1",
            "TRAGR": "0001",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {
            "MTVFP": "02", "LADGR": "0001", "EKGRP": "007",
            "KAUTB": "X", "TAXIM": "1",
        },
        "valores_fijos_centro_A120": {
            "MTVFP": "02", "LADGR": "0001", "EKGRP": "007",
            "KAUTB": "X", "TAXIM": "1",
        },
        "cadenas": {
            "org_3001": {"canales": ["30", "40", "50"], "centro": "A130", "MTPOS": "NORM", "KTGRM": "03"},
            "org_1001": {"canales": ["10", "20", "30", "40", "50"], "centro": "A120", "MTPOS": "NORM", "KTGRM": "03"},
        },
        "fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "prevision": False,
        "lugares_almacenamiento": {
            "A130": ["0040", "0041", "0042", "0043"],
            "A120": ["0030", "0031"],
        },
        "area_planificacion": False,
        "valoracion": [
            {"BWKEY": "A130", "BKLAS": "3400", "VPRSV": "V", "VERPR": "0.04", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A120", "BKLAS": "3400", "VPRSV": "V", "VERPR": "0.04", "STPRS": "", "PEINH": "1"},
        ],
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "VOLUM", "TAXIM", "KTGRM"],
        "campos_modificacion": ["MATNR", "MAKTX", "TEXTO_LARGO", "MSTAE"],
    },

    "ZSER_C": {
        "vistas_basicos": ["B", "V", "C", "CO"],
        "valores_fijos_basicos": {
            "MTART": "ZSER",
            "SPRAS": "ES",
            "SPART": "S4",
            "MTPOS": "LEIS",
            "EKWSL": "1",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {
            "MTVFP": "KP", "EKGRP": "006", "KAUTB": "X", "TAXIM": "1",
        },
        "valores_fijos_centro_A110": {
            "MTVFP": "KP", "EKGRP": "006", "KAUTB": "X", "TAXIM": "1",
        },
        "cadenas": {
            "org_3001": {"canales": ["30", "40", "50"], "centro": "A130", "MTPOS": "LEIS", "KTGRM": "04"},
            "org_1001": {"canales": ["10", "20", "30", "40", "50"], "centro": "A110", "MTPOS": "LEIS", "KTGRM": "04"},
        },
        "fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "prevision": False,
        "lugares_almacenamiento": {},
        "area_planificacion": False,
        "valoracion": [
            {"BWKEY": "A130", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
        ],
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "TAXIM", "KTGRM"],
        "campos_modificacion": ["MATNR", "MAKTX", "TEXTO_LARGO", "MSTAE"],
    },

    "ZSER_NC": {
        "vistas_basicos": ["B", "V", "CO"],
        "valores_fijos_basicos": {
            "MTART": "ZSER",
            "SPRAS": "ES",
            "SPART": "S4",
            "MTPOS": "LEIS",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {
            "TAXIM": "1",
        },
        "valores_fijos_centro_A110": {
            "TAXIM": "1",
        },
        "cadenas": {
            "org_3001": {"canales": ["30", "40", "50"], "centro": "A130", "MTPOS": "LEIS", "KTGRM": "04"},
            "org_1001": {"canales": ["10", "20", "30", "40", "50"], "centro": "A110", "MTPOS": "LEIS", "KTGRM": "04"},
        },
        "fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "prevision": False,
        "lugares_almacenamiento": {},
        "area_planificacion": False,
        "valoracion": [
            {"BWKEY": "A130", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
        ],
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "TAXIM", "KTGRM"],
        "campos_modificacion": ["MATNR", "MAKTX", "TEXTO_LARGO", "MSTAE"],
    },

    "ZNOA": {
        "vistas_basicos": ["B", "C", "CO"],
        "valores_fijos_basicos": {
            "MTART": "ZNOA",
            "SPRAS": "ES",
            "MTPOS": "NLAG",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {"EKGRP": "006", "KAUTB": "X", "TAXIM": "1"},
        "valores_fijos_centro_A110": {"EKGRP": "006", "KAUTB": "X", "TAXIM": "1"},
        "valores_fijos_centro_A120": {"EKGRP": "006", "KAUTB": "X", "TAXIM": "1"},
        "cadenas": None,
        "fiscal": None,
        "prevision": False,
        "lugares_almacenamiento": {},
        "area_planificacion": False,
        "valoracion": [
            {"BWKEY": "A110", "BKLAS": "3507", "VPRSV": "V", "VERPR": "1", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A120", "BKLAS": "3507", "VPRSV": "V", "VERPR": "1", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A130", "BKLAS": "3507", "VPRSV": "V", "VERPR": "1", "STPRS": "", "PEINH": "1"},
        ],
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "TAXIM"],
        "campos_modificacion": ["MATNR", "MAKTX", "TEXTO_LARGO", "MSTAE"],
    },

    "ZCOM": {
        "vistas_basicos": ["B", "V", "A"],
        "valores_fijos_basicos": {
            "MTART": "ZCOM",
            "SPRAS": "ES",
            "SPART": "S2",
            "MTPOS": "ERLA",
            "TRAGR": "0001",
            "MSTAE": "/",
        },
        "valores_fijos_centro_A130": {
            "MTVFP": "KP", "KOKRS": "AR01", "PRCTR": "AR01021400",
            "LADGR": "0001",
        },
        "cadenas": {
            "org_3001": {"canales": ["30", "40", "50"], "centro": "A130", "MTPOS": "ERLA", "KTGRM": "03"},
        },
        "fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "prevision": False,
        "lugares_almacenamiento": {
            "A130": ["0040", "0041", "0042", "0043"],
        },
        "area_planificacion": False,
        "valoracion": [],  # sin datos de valoración en ZCOM
        "campos_entrada": ["MATNR", "MAKTX", "MATKL", "PRDHA", "VOLUM", "TAXIM", "KTGRM"],
        "campos_modificacion": ["MATNR", "MAKTX", "TEXTO_LARGO", "MSTAE"],
    },
}

# Mapeo de vistas a nombres de columna en la hoja Datos básicos
VISTA_COLUMNAS = {
    "B":   "Vista de Datos básicos",
    "V":   "Vista de Ventas",
    "C":   "Vista de compras",
    "MRP": "Vista de MRP",
    "P":   "Vista de pronóstico",
    "A":   "Vista de almacenamiento",
    "WM":  "Vista de WM",
    "CO":  "Vista de contabilidad",
    "MRP_AREA": "Asignar área MRP",
}
