# =============================================================================
# config.py — Configuración central
# =============================================================================

# ---------------------------------------------------------------------------
# Opciones de campos con desplegable
# ---------------------------------------------------------------------------
OPCIONES = {
    "EKGRP_ZMED_ZNOM": [f"{i:03d}" for i in range(1, 6)],        # 001-005
    "EKGRP_ZINS":      ["007"],
    "EKGRP_ZSER_C":    ["006"],
    "TAXIM_FULL":      [str(i) for i in range(1, 8)],             # 1-7
    "TAXIM_6":         [str(i) for i in range(1, 8)],             # 1-7 (mismo rango completo)
    "TAXIM_1":         [str(i) for i in range(1, 8)],             # 1-7
    "KTGRM_ZMED":      ["01", "02"],
    "KTGRM_ZNOM_ZINS": ["03"],
    "KTGRM_ZSER":      ["04", "05"],
    "KTGRM_ZCOM":      ["03"],
    "SPART_ZMED":      ["S1"],
    "SPART_ZNOM":      ["S2", "S3"],
    "SPART_ZINS":      ["S2"],
    "SPART_ZSER":      ["S4"],
    "SPART_ZCOM":      ["S2"],
}

CENTROS_DISPONIBLES = {
    "ZMED":    ["A110", "A130"],
    "ZNOM":    ["A110", "A120", "A130"],
    "ZINS":    ["A120", "A130"],
    "ZSER_C":  ["A110", "A130"],
    "ZSER_NC": ["A110", "A130"],
    "ZNOA":    ["A110", "A120", "A130"],
    "ZCOM":    ["A110", "A130"],
}

# ---------------------------------------------------------------------------
# Mapa de centros (sucursales): WERKS → KOKRS / PRCTR
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Configuración por tipo de material
# Cada entrada define todo lo necesario para los 3 flujos
# ---------------------------------------------------------------------------
TIPOS_MATERIAL = {

    "ZMED": {
        # ── Datos básicos ──────────────────────────────────────────────────
        "MTART": "ZMED",
        "SPART": "S1",
        "XCHPF": "X",          # gestión de lotes
        "MTPOS": "NORM",
        "VOLEH": "CM3",
        "EKWSL": "1",
        "TRAGR": "0001",
        "IPRKZ": "D",
        "MHDRZ": "270",
        "SERIAL": "TRAZ",
        # vistas activas en centros logísticos
        "vistas_CL": ["B","V","C","MRP","P","A","WM","CO","MRPAREA"],
        # vistas activas en sucursales
        "vistas_SUC": ["A"],
        # vistas activas en modificación
        "vistas_MOD": ["B","C"],
        # ── Centros logísticos ─────────────────────────────────────────────
        "CL_centros": [
            {
                "WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400",
                "DISMM": "V1", "DISPO": "Z01", "MTVFP": "02",
                "LADGR": "0001", "KAUTB": "X",
                "DISGR": "0000", "MINBE": "10", "DISLS": "EX",
                "BSTMI": "1", "BESKZ": "F", "LGFSB": "0040", "PLIFZ": "4",
                "ekgrp_opciones": OPCIONES["EKGRP_ZMED_ZNOM"],
                "taxim_opciones": OPCIONES["TAXIM_6"],
            },
            {
                "WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200",
                "MTVFP": "02", "LADGR": "0001", "KAUTB": "X",
                "XCHPF": "X", "SERNP": "TRAZ",
                "ekgrp_opciones": OPCIONES["EKGRP_ZMED_ZNOM"],
                "taxim_opciones": OPCIONES["TAXIM_6"],
            },
        ],
        "CL_cadenas": [
            {"VKORG": "3001", "canales": ["30","40","50"], "DWERK": "A130", "MTPOS": "NORM"},
            {"VKORG": "1001", "canales": ["10","20","30","40","50"], "DWERK": "A110", "MTPOS": "NORM"},
        ],
        "CL_ktgrm_opciones": OPCIONES["KTGRM_ZMED"],
        "CL_fiscal": {"TAXM1": "0", "TAXM2": "0"},
        "CL_prevision": True,
        "CL_lugares": {"A130": ["0040","0041","0042","0043"], "A110": ["0010","0011","0020","0021","0022"]},
        "CL_area_planif": True,
        "CL_valoracion": [
            {"BWKEY": "A130", "BKLAS": "3101", "VPRSV": "V", "VERPR": "20",  "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3101", "VPRSV": "V", "VERPR": "200", "STPRS": "", "PEINH": "1"},
        ],
        # ── Sucursales ─────────────────────────────────────────────────────
        "SUC_datos_centro": False,   # solo almacenamiento, sin campos extra
        "SUC_valoracion": False,
        # ── Modificación ───────────────────────────────────────────────────
        "MOD_campos": ["MAKTX", "PRDHA", "VOLUM", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {"MTPOS": "NORM", "VOLEH": "CM3"},
    },

    "ZNOM": {
        "MTART": "ZNOM",
        "SPART": "S2",          # puede ser S2 o S3 — el usuario elige
        "SPART_opciones": ["S2","S3"],
        "XCHPF": "X",          # gestión de lotes
        "MTPOS": "NORM",
        "VOLEH": "CM3",
        "EKWSL": "1",
        "TRAGR": "0001",
        "IPRKZ": "D",
        "MHDRZ": "270",
        "vistas_CL":  ["B","V","C","MRP","P","A","WM","CO","MRPAREA"],
        "vistas_SUC": ["A"],
        "vistas_MOD": ["B","C"],
        "CL_centros": [
            {
                "WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400",
                "DISMM": "V1", "DISPO": "Z01", "MTVFP": "02",
                "LADGR": "0001", "KAUTB": "X",
                "DISGR": "0000", "MINBE": "10", "DISLS": "EX",
                "BSTMI": "1", "BESKZ": "F", "LGFSB": "0040", "PLIFZ": "4",
                "ekgrp_opciones": OPCIONES["EKGRP_ZMED_ZNOM"],
                "taxim_opciones": OPCIONES["TAXIM_6"],
            },
            {
                "WERKS": "A120", "KOKRS": "AR01", "PRCTR": "AR01031200",
                "MTVFP": "02", "LADGR": "0001", "KAUTB": "X",
                "XCHPF": "X",
                "ekgrp_opciones": OPCIONES["EKGRP_ZMED_ZNOM"],
                "taxim_opciones": OPCIONES["TAXIM_6"],
            },
            {
                "WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200",
                "MTVFP": "02", "LADGR": "0001", "KAUTB": "X",
                "XCHPF": "X", "SERNP": "TRAZ",
                "ekgrp_opciones": OPCIONES["EKGRP_ZMED_ZNOM"],
                "taxim_opciones": OPCIONES["TAXIM_6"],
            },
        ],
        "CL_cadenas": [
            {"VKORG": "3001", "canales": ["30","40","50"], "DWERK": "A130", "MTPOS": "NORM"},
            {"VKORG": "1001", "canales": ["10","20","30","40","50"], "DWERK": "A120", "MTPOS": "NORM"},
            {"VKORG": "1001", "canales": ["10","20","30","40","50"], "DWERK": "A110", "MTPOS": "NORM"},
        ],
        "CL_ktgrm_opciones": OPCIONES["KTGRM_ZNOM_ZINS"],
        "CL_fiscal": {"TAXM1": "0", "TAXM2": "0"},
        "CL_prevision": True,
        "CL_lugares": {"A130": ["0040","0041","0042","0043"], "A120": ["0030","0031"], "A110": ["0010","0011","0020","0021","0022"]},
        "CL_area_planif": True,
        "CL_valoracion": [
            {"BWKEY": "A130", "BKLAS": "3300", "VPRSV": "V", "VERPR": "20",  "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A120", "BKLAS": "3300", "VPRSV": "V", "VERPR": "200", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3300", "VPRSV": "V", "VERPR": "200", "STPRS": "", "PEINH": "1"},
        ],
        "SUC_datos_centro": False,
        "SUC_valoracion": False,
        "MOD_campos": ["MAKTX", "PRDHA", "VOLUM", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {"MTPOS": "NORM", "VOLEH": "CM3"},
    },

    "ZINS": {
        "MTART": "ZINS",
        "SPART": "S2",
        "MTPOS": "NORM",
        "VOLEH": "CM3",
        "EKWSL": "1",
        "TRAGR": "0001",
        "vistas_CL":  ["B","V","C","A","CO"],
        "vistas_SUC": ["A","CO"],
        "vistas_MOD": ["B"],
        "CL_centros": [
            {
                "WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400",
                "MTVFP": "02", "LADGR": "0001", "KAUTB": "X",
                "ekgrp_opciones": OPCIONES["EKGRP_ZINS"],
                "taxim_opciones": OPCIONES["TAXIM_FULL"],
            },
            {
                "WERKS": "A120", "KOKRS": "AR01", "PRCTR": "AR01031200",
                "MTVFP": "02", "LADGR": "0001", "KAUTB": "X",
                "ekgrp_opciones": OPCIONES["EKGRP_ZINS"],
                "taxim_opciones": OPCIONES["TAXIM_FULL"],
            },
        ],
        "CL_cadenas": [
            {"VKORG": "3001", "canales": ["30","40","50"], "DWERK": "A130", "MTPOS": "NORM"},
            {"VKORG": "1001", "canales": ["10","20","30","40","50"], "DWERK": "A120", "MTPOS": "NORM"},
        ],
        "CL_ktgrm_opciones": OPCIONES["KTGRM_ZNOM_ZINS"],
        "CL_fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "CL_prevision": False,
        "CL_lugares": {"A130": ["0040","0041","0042","0043"], "A120": ["0030","0031"]},
        "CL_area_planif": False,
        "CL_valoracion": [
            {"BWKEY": "A130", "BKLAS": "3400", "VPRSV": "V", "VERPR": "0.04", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A120", "BKLAS": "3400", "VPRSV": "V", "VERPR": "0.04", "STPRS": "", "PEINH": "1"},
        ],
        "SUC_datos_centro": True,
        "SUC_ekgrp": "007",
        "SUC_kautb": "X",
        "SUC_taxim": "1",
        "SUC_valoracion": True,
        "SUC_bklas": "3400", "SUC_vprsv": "V", "SUC_verpr": "0.04", "SUC_peinh": "1",
        "MOD_campos": ["MAKTX", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {},
    },

    "ZSER_C": {
        "MTART": "ZSER",
        "SPART": "S4",
        "MTPOS": "LEIS",
        "EKWSL": "1",
        "vistas_CL":  ["B","V","C","CO"],
        "vistas_SUC": [],
        "vistas_MOD": ["B"],
        "CL_centros": [
            {
                "WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400",
                "MTVFP": "KP", "KAUTB": "X",
                "ekgrp_opciones": OPCIONES["EKGRP_ZSER_C"],
                "taxim_opciones": OPCIONES["TAXIM_FULL"],
            },
            {
                "WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200",
                "MTVFP": "KP", "KAUTB": "X",
                "ekgrp_opciones": OPCIONES["EKGRP_ZSER_C"],
                "taxim_opciones": OPCIONES["TAXIM_FULL"],
            },
        ],
        "CL_cadenas": [
            {"VKORG": "3001", "canales": ["30","40","50"], "DWERK": "A130", "MTPOS": "LEIS"},
            {"VKORG": "1001", "canales": ["10","20","30","40","50"], "DWERK": "A110", "MTPOS": "LEIS"},
        ],
        "CL_ktgrm_opciones": OPCIONES["KTGRM_ZSER"],
        "CL_fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "CL_prevision": False,
        "CL_lugares": {},
        "CL_area_planif": False,
        "CL_valoracion": [
            {"BWKEY": "A130", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
        ],
        "SUC_datos_centro": True,
        "SUC_ekgrp": "006",
        "SUC_kautb": "",
        "SUC_taxim": "1",
        "SUC_mtvfp": "KP",
        "vistas_SUC": ["V", "C", "CO"],
        "SUC_valoracion": True,
        "SUC_bklas": "3233",
        "SUC_vprsv": "S",
        "SUC_verpr": "",
        "SUC_stprs": "4",
        "SUC_peinh": "1",
        "MOD_campos": ["MAKTX", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {},
    },

    "ZSER_NC": {
        "MTART": "ZSER",
        "SPART": "S4",
        "MTPOS": "LEIS",
        "vistas_CL":  ["B","V","CO"],
        "vistas_SUC": [],
        "vistas_MOD": ["B"],
        "CL_centros": [
            {
                "WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400",
                "taxim_opciones": OPCIONES["TAXIM_FULL"],
            },
            {
                "WERKS": "A110", "KOKRS": "AR01", "PRCTR": "AR01031200",
                "taxim_opciones": OPCIONES["TAXIM_FULL"],
            },
        ],
        "CL_cadenas": [
            {"VKORG": "3001", "canales": ["30","40","50"], "DWERK": "A130", "MTPOS": "LEIS"},
            {"VKORG": "1001", "canales": ["10","20","30","40","50"], "DWERK": "A110", "MTPOS": "LEIS"},
        ],
        "CL_ktgrm_opciones": OPCIONES["KTGRM_ZSER"],
        "CL_fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "CL_prevision": False,
        "CL_lugares": {},
        "CL_area_planif": False,
        "CL_valoracion": [
            {"BWKEY": "A130", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
            {"BWKEY": "A110", "BKLAS": "3233", "VPRSV": "S", "VERPR": "", "STPRS": "4", "PEINH": "1"},
        ],
        "SUC_datos_centro": False,
        "vistas_SUC": ["V"],
        "SUC_valoracion": False,
        "MOD_campos": ["MAKTX", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {},
    },

    "ZNOA": {
        "MTART": "ZNOA",
        "MTPOS": "NLAG",
        "vistas_CL":  ["B","C","CO"],
        "vistas_SUC": [],
        "vistas_MOD": ["B"],
        "CL_centros": [
            {"WERKS": "A110", "EKGRP": "006", "KAUTB": "X", "taxim_opciones": OPCIONES["TAXIM_FULL"]},
            {"WERKS": "A120", "EKGRP": "006", "KAUTB": "X", "taxim_opciones": OPCIONES["TAXIM_FULL"]},
            {"WERKS": "A130", "EKGRP": "006", "KAUTB": "X", "taxim_opciones": OPCIONES["TAXIM_FULL"]},
        ],
        "CL_cadenas": None,
        "CL_fiscal": None,
        "CL_prevision": False,
        "CL_lugares": {},
        "CL_area_planif": False,
        "CL_valoracion": [
            {"BWKEY": "A110", "BKLAS": "3507", "VPRSV": "V", "VERPR": "1", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A120", "BKLAS": "3507", "VPRSV": "V", "VERPR": "1", "STPRS": "", "PEINH": "1"},
            {"BWKEY": "A130", "BKLAS": "3507", "VPRSV": "V", "VERPR": "1", "STPRS": "", "PEINH": "1"},
        ],
        "SUC_datos_centro": True,
        "SUC_ekgrp": "007",
        "SUC_kautb": "X",
        "SUC_taxim_opciones": [str(i) for i in range(1, 7)],
        "SUC_valoracion": True,
        "SUC_bklas": "3507",
        "SUC_vprsv": "V",
        "SUC_verpr": "1",
        "SUC_peinh": "1",
        "ZNOA_incluye_sucursales_en_CL": True,
        "MOD_campos": ["MAKTX", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {},
    },

    "ZCOM": {
        "MTART": "ZCOM",
        "SPART": "S2",
        "MTPOS": "ERLA",
        "TRAGR": "0001",
        "vistas_CL":  ["B","V","A"],
        "vistas_SUC": [],
        "vistas_MOD": ["B"],
        "CL_centros": [
            {
                "WERKS": "A130", "KOKRS": "AR01", "PRCTR": "AR01021400",
                "MTVFP": "KP", "LADGR": "0001",
            },
        ],
        "CL_cadenas": [
            {"VKORG": "3001", "canales": ["30","40","50"], "DWERK": "A130", "MTPOS": "ERLA"},
        ],
        "CL_ktgrm_opciones": OPCIONES["KTGRM_ZCOM"],
        "CL_fiscal": {"TAXM1": "1", "TAXM2": "0"},
        "CL_prevision": False,
        "CL_lugares": {"A130": ["0040","0041","0042","0043"]},
        "CL_area_planif": False,
        "CL_valoracion": [],
        "SUC_datos_centro": False,
        "SUC_valoracion": False,
        "MOD_campos": ["MAKTX", "VOLUM", "TEXTO_LARGO", "MSTAE"],
        "MOD_fijos": {},
        "VOLEH": "CM3",
    },
}

# Nombres de columna para las vistas (fila 1 del .txt)
VISTA_NOMBRES = {
    "B":       "Vista de Datos básicos",
    "V":       "Vista de Ventas",
    "C":       "Vista de compras",
    "MRP":     "Vista de MRP",
    "P":       "Vista de pronóstico",
    "A":       "Vista de almacenamiento",
    "WM":      "Vista de WM",
    "CO":      "Vista de contabilidad",
    "MRPAREA": "Asignar área MRP",
}
