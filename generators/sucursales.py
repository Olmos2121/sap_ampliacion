"""
generators/sucursales.py
Genera el Excel de ampliación de sucursales.
Hojas: Datos básicos (vista almacenamiento), Datos de centro (los ~70 centros),
       Datos de valoración (solo ZINS).
"""
import pandas as pd
from collections import OrderedDict
from config import TIPOS_MATERIAL, CENTRO_BENEFICIO_MAP
from generators.utils import escribir_excel

# Configuración por tipo de material para sucursales
SUCURSALES_CFG = {
    "ZMED": {
        "vistas_basicos": "A",       # solo vista almacenamiento
        "datos_centro": False,       # ZMED y ZNOM no llevan datos de centro en suc.
        "valoracion": False,
    },
    "ZNOM": {
        "vistas_basicos": "A",
        "datos_centro": False,
        "valoracion": False,
    },
    "ZINS": {
        "vistas_basicos": "A",
        "datos_centro": True,
        "ekgrp": "7",
        "kautb": "X",
        "taxim": "1",
        "valoracion": True,
        "bklas": "3400",
        "vprsv": "V",
        "verpr": "0.04",
        "peinh": "1",
    },
}


def generar_sucursales(df_input: pd.DataFrame, tipo_mat: str) -> bytes:
    suc_cfg = SUCURSALES_CFG.get(tipo_mat, {})
    hojas = OrderedDict()

    hojas["Datos básicos"] = _datos_basicos_suc(df_input, tipo_mat)
    hojas["Datos de centro"] = _datos_centro_suc(df_input, tipo_mat, suc_cfg)
    if suc_cfg.get("valoracion"):
        hojas["Datos de valoración"] = _datos_valoracion_suc(df_input, suc_cfg)

    return escribir_excel(hojas)


def _datos_basicos_suc(df_input: pd.DataFrame, tipo_mat: str) -> pd.DataFrame:
    """Solo marca la vista de Almacenamiento en datos básicos."""
    rows = []
    for _, mat in df_input.iterrows():
        rows.append({
            "Número de producto": mat["MATNR"],
            "Vista de Datos básicos": "",
            "Vista de Ventas": "",
            "Vista de compras": "",
            "Vista de MRP": "",
            "Vista de pronóstico": "",
            "Vista de almacenamiento": "X",
            "Vista de WM": "",
            "Vista de contabilidad": "X" if tipo_mat == "ZINS" else "",
            "Asignar área MRP": "",
        })
    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = [
        "MATNR", "", "", "", "", "", "", "", "", ""
    ]
    return df


def _datos_centro_suc(df_input: pd.DataFrame, tipo_mat: str, suc_cfg: dict) -> pd.DataFrame:
    """
    Genera una fila por cada material x cada sucursal del mapa.
    Para ZMED/ZNOM solo se pone KOKRS y PRCTR (sin otros campos).
    Para ZINS además EKGRP, KAUTB, TAXIM.
    """
    rows = []
    for _, mat in df_input.iterrows():
        for werks, centro_data in CENTRO_BENEFICIO_MAP.items():
            row = {
                "Número de producto": mat["MATNR"],
                "Centro": werks,
                "Tipo de MRP": "",
                "Planificador de necesidades": "",
                "Verificación de disponibilidad": "",
                "Sociedad CO": centro_data["KOKRS"],
                "Centro de beneficio": centro_data["PRCTR"],
                "Indicador sol.gestión de lotes": "",
                "Perfil Serie": "",
                "Grupo de carga": "",
                "Grupo de compra": suc_cfg.get("ekgrp", "") if suc_cfg.get("datos_centro") else "",
                "Pedido automático permitido": suc_cfg.get("kautb", "") if suc_cfg.get("datos_centro") else "",
                "Indicador de impuestos": suc_cfg.get("taxim", "") if suc_cfg.get("datos_centro") else "",
                "Grupo MRP": "",
                "Punto de reorganización": "",
                "Cálculo de tamaño de lote": "",
                "Tamaño de lote mínimo": "",
                "Tamaño de lote máximo": "",
                "Tamaño de lote fijo": "",
                "Clase de aprovisionamiento": "",
                "Almacén estándar p.aprovisionam.externo": "",
                "Hora de entrega planificada": "",
            }
            rows.append(row)

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = [
        "MATNR", "WERKS", "DISMM", "DISPO", "MTVFP", "KOKRS", "PRCTR",
        "XCHPF", "SERNP", "LADGR", "EKGRP", "KAUTB", "TAXIM", "DISGR",
        "MINBE", "DISLS", "BSTMI", "BSTMA", "BSTFE", "BESKZ", "LGFSB", "PLIFZ"
    ]
    return df


def _datos_valoracion_suc(df_input: pd.DataFrame, suc_cfg: dict) -> pd.DataFrame:
    """Valoración para ZINS: una fila por material x cada sucursal."""
    rows = []
    for _, mat in df_input.iterrows():
        for werks in CENTRO_BENEFICIO_MAP.keys():
            rows.append({
                "Número de producto": mat["MATNR"],
                "Área de valoración": werks,
                "Categoría de valoración": suc_cfg["bklas"],
                "Control de precios": suc_cfg["vprsv"],
                "Moneda": "ARS",
                "Media variable de precio de inventario": suc_cfg["verpr"],
                "Precio estándar de precio de inventario": "",
                "Unidad de precio": suc_cfg["peinh"],
            })

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = [
        "MATNR", "BWKEY", "BKLAS", "VPRSV", "WAERS", "VERPR", "STPRS", "PEINH"
    ]
    return df
