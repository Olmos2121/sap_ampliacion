"""
generators/modificacion.py
Genera el Excel de modificación de datos básicos.
Solo genera la hoja Datos básicos con los campos modificables:
MAKTX, PRDHA, VOLUM, TEXTO_LARGO, MSTAE.
"""
import pandas as pd
from collections import OrderedDict
from config import TIPOS_MATERIAL, VISTA_COLUMNAS
from generators.utils import escribir_excel


# Vistas que se activan para modificación por tipo de material
VISTAS_MOD = {
    "ZMED":   ["B", "C"],
    "ZNOM":   ["B", "C"],
    "ZINS":   ["B"],
    "ZSER_C": ["B"],
    "ZSER_NC":["B"],
    "ZNOA":   ["B"],
    "ZCOM":   ["B"],
}

# Campos que el tipo de material permite modificar
CAMPOS_MOD = {
    "ZMED":    {"MAKTX": True, "PRDHA": True, "VOLUM": True, "TEXTO_LARGO": True, "MSTAE": True},
    "ZNOM":    {"MAKTX": True, "PRDHA": True, "VOLUM": True, "TEXTO_LARGO": True, "MSTAE": True},
    "ZINS":    {"MAKTX": True, "PRDHA": False, "VOLUM": False, "TEXTO_LARGO": True, "MSTAE": True},
    "ZSER_C":  {"MAKTX": True, "PRDHA": False, "VOLUM": False, "TEXTO_LARGO": True, "MSTAE": True},
    "ZSER_NC": {"MAKTX": True, "PRDHA": False, "VOLUM": False, "TEXTO_LARGO": True, "MSTAE": True},
    "ZNOA":    {"MAKTX": True, "PRDHA": False, "VOLUM": False, "TEXTO_LARGO": True, "MSTAE": True},
    "ZCOM":    {"MAKTX": True, "PRDHA": False, "VOLUM": False, "TEXTO_LARGO": True, "MSTAE": True},
}

# Valores fijos de campos no modificables (se heredan del tipo de material)
VALORES_FIJOS_MOD = {
    "ZMED":    {"MTPOS": "NORM", "VOLEH": "CM3"},
    "ZNOM":    {"MTPOS": "NORM", "VOLEH": "CM3"},
    "ZINS":    {},
    "ZSER_C":  {},
    "ZSER_NC": {},
    "ZNOA":    {},
    "ZCOM":    {},
}


def generar_modificacion(df_input: pd.DataFrame, tipo_mat: str) -> bytes:
    hojas = OrderedDict()
    hojas["Datos básicos"] = _datos_basicos_mod(df_input, tipo_mat)
    return escribir_excel(hojas)


def _datos_basicos_mod(df_input: pd.DataFrame, tipo_mat: str) -> pd.DataFrame:
    vistas = VISTAS_MOD.get(tipo_mat, ["B"])
    campos_mod = CAMPOS_MOD.get(tipo_mat, {})
    fijos = VALORES_FIJOS_MOD.get(tipo_mat, {})

    rows = []
    for _, mat in df_input.iterrows():
        row = {"Número de producto": mat["MATNR"]}

        # Vistas activas
        for codigo, col_nombre in VISTA_COLUMNAS.items():
            if codigo == "MRP_AREA":
                row[col_nombre] = ""
            else:
                row[col_nombre] = "X" if codigo in vistas else ""

        row["Clase de producto"] = ""
        row["Grupo de productos"] = ""

        # Descripción — siempre modificable si viene en el input
        row["Descripción"] = mat.get("MAKTX", "") if campos_mod.get("MAKTX") else ""
        row["Código de idioma"] = "ES" if mat.get("MAKTX", "") else ""

        row["Partición"] = ""
        row["Jerarquía de productos"] = mat.get("PRDHA", "") if campos_mod.get("PRDHA") else ""
        row["Indicador Gestión de lotes"] = ""
        row["Grupo de clases de artículo general"] = fijos.get("MTPOS", "")
        row["Volumen"] = mat.get("VOLUM", "") if campos_mod.get("VOLUM") else ""
        row["Unidad de volumen"] = fijos.get("VOLEH", "") if mat.get("VOLUM", "") else ""
        row["Clave de valor de compras"] = ""
        row["Grupo de transporte"] = ""
        row["Indicador de periodo para caducidad"] = ""
        row["Caducidad residual mínima"] = ""
        row["Perfil Serie"] = ""
        row["Texto largo"] = mat.get("TEXTO_LARGO", "") if campos_mod.get("TEXTO_LARGO") else ""
        row["Bloqueo de material"] = mat.get("MSTAE", "") if campos_mod.get("MSTAE") else ""

        rows.append(row)

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = [
        "MATNR", "", "", "", "", "", "", "", "", "", "MTART", "MATKL",
        "MAKTX", "SPRAS", "SPART", "PRDHA", "XCHPF", "MTPOS", "VOLUM",
        "VOLEH", "EKWSL", "TRAGR", "IPRKZ", "MHDRZ", "SERIAL", "", "MSTAE"
    ]
    return df
