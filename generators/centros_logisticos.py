"""
generators/centros_logisticos.py
Genera el Excel de ampliación de centros logísticos para cualquier tipo de material.
Hojas: Datos básicos, Datos de centro, Cadenas de distribución, Clasificación fiscal,
       Datos de previsión, Lugares de almacenamiento, Área planif.nec., Datos de valoración
"""
import pandas as pd
from collections import OrderedDict
from config import TIPOS_MATERIAL, CENTROS_LOGISTICOS
from generators.utils import (
    escribir_excel,
    construir_datos_basicos,
    construir_clasificacion_fiscal,
    construir_datos_prevision,
    construir_area_planificacion,
)


def generar_centros_logisticos(df_input: pd.DataFrame, tipo_mat: str) -> bytes:
    cfg = TIPOS_MATERIAL[tipo_mat]
    hojas = OrderedDict()

    hojas["Datos básicos"] = _datos_basicos(df_input, cfg)
    hojas["Datos de centro"] = _datos_centro(df_input, cfg, tipo_mat)
    hojas["Cadenas de distribución"] = _cadenas(df_input, cfg)
    hojas["Clasificación fiscal"] = construir_clasificacion_fiscal(df_input, cfg)
    hojas["Datos de previsión"] = construir_datos_prevision(df_input, cfg)
    hojas["Lugares de almacenamiento"] = _lugares_almacenamiento(df_input, cfg)
    hojas["Área planific.nec."] = construir_area_planificacion(df_input, cfg)
    hojas["Datos de valoración"] = _datos_valoracion(df_input, cfg)

    return escribir_excel(hojas)


def _datos_basicos(df_input: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    return construir_datos_basicos(df_input, cfg)


def _datos_centro(df_input: pd.DataFrame, cfg: dict, tipo_mat: str) -> pd.DataFrame:
    centros = CENTROS_LOGISTICOS.get(tipo_mat, [])
    rows = []

    for _, mat in df_input.iterrows():
        for centro_info in centros:
            werks = centro_info["WERKS"]
            key = f"valores_fijos_centro_{werks}"
            fijos = cfg.get(key, {})

            # Algunos campos variables vienen del input (ej: EKGRP, TAXIM)
            ekgrp = mat.get(f"EKGRP_{werks}", mat.get("EKGRP", fijos.get("EKGRP", "")))
            taxim = mat.get("TAXIM", fijos.get("TAXIM", ""))

            row = {
                "Número de producto": mat["MATNR"],
                "Centro": werks,
                "Tipo de MRP": fijos.get("DISMM", ""),
                "Planificador de necesidades": fijos.get("DISPO", ""),
                "Verificación de disponibilidad": fijos.get("MTVFP", ""),
                "Sociedad CO": centro_info.get("KOKRS", fijos.get("KOKRS", "")),
                "Centro de beneficio": centro_info.get("PRCTR", fijos.get("PRCTR", "")),
                "Indicador sol.gestión de lotes": fijos.get("XCHPF", ""),
                "Perfil Serie": fijos.get("SERNP", ""),
                "Grupo de carga": fijos.get("LADGR", ""),
                "Grupo de compra": ekgrp,
                "Pedido automático permitido": fijos.get("KAUTB", ""),
                "Indicador de impuestos": taxim,
                "Grupo MRP": fijos.get("DISGR", ""),
                "Punto de reorganización": fijos.get("MINBE", ""),
                "Cálculo de tamaño de lote": fijos.get("DISLS", ""),
                "Tamaño de lote mínimo": fijos.get("BSTMI", ""),
                "Tamaño de lote máximo": fijos.get("BSTMA", ""),
                "Tamaño de lote fijo": fijos.get("BSTFE", ""),
                "Clase de aprovisionamiento": fijos.get("BESKZ", ""),
                "Almacén estándar p.aprovisionam.externo": fijos.get("LGFSB", ""),
                "Hora de entrega planificada": fijos.get("PLIFZ", ""),
            }
            rows.append(row)

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = [
        "MATNR", "WERKS", "DISMM", "DISPO", "MTVFP", "KOKRS", "PRCTR",
        "XCHPF", "SERNP", "LADGR", "EKGRP", "KAUTB", "TAXIM", "DISGR",
        "MINBE", "DISLS", "BSTMI", "BSTMA", "BSTFE", "BESKZ", "LGFSB", "PLIFZ"
    ]
    return df


def _cadenas(df_input: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    cadenas_cfg = cfg.get("cadenas")
    if not cadenas_cfg:
        return pd.DataFrame()

    rows = []
    for _, mat in df_input.iterrows():
        prodh = mat.get("PRDHA", "")
        for org_key, org_cfg in cadenas_cfg.items():
            vkorg = "3001" if "3001" in org_key else "1001"
            for canal in org_cfg["canales"]:
                # KTGRM puede venir del input o del config
                ktgrm = mat.get("KTGRM", org_cfg.get("KTGRM", "01"))
                rows.append({
                    "Número de producto": mat["MATNR"],
                    "Organización de ventas": vkorg,
                    "Canal de distribución": canal,
                    "Centro suministrador": org_cfg["centro"],
                    "Grupo de categoría de posición": org_cfg.get("MTPOS", ""),
                    "Grupo de imputación": ktgrm,
                    "Jerarquía de productos": prodh,
                })

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = ["MATNR", "VKORG", "VTWEG", "DWERK", "MTPOS", "KTGRM", "PRODH"]
    return df


def _lugares_almacenamiento(df_input: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    lugares = cfg.get("lugares_almacenamiento", {})
    if not lugares:
        return pd.DataFrame()

    rows = []
    for _, mat in df_input.iterrows():
        for centro, ubicaciones in lugares.items():
            for lgort in ubicaciones:
                rows.append({
                    "Número de producto": mat["MATNR"],
                    "Centro": centro,
                    "Ubicación de almacén": lgort,
                })

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = ["MATNR", "WERKS", "LGORT"]
    return df


def _datos_valoracion(df_input: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    val_cfg = cfg.get("valoracion", [])
    if not val_cfg:
        return pd.DataFrame()

    rows = []
    for _, mat in df_input.iterrows():
        for val in val_cfg:
            rows.append({
                "Número de producto": mat["MATNR"],
                "Área de valoración": val["BWKEY"],
                "Categoría de valoración": val["BKLAS"],
                "Control de precios": val["VPRSV"],
                "Moneda": "ARS",
                "Media variable de precio de inventario": val.get("VERPR", ""),
                "Precio estándar de precio de inventario": val.get("STPRS", ""),
                "Unidad de precio": val.get("PEINH", "1"),
            })

    df = pd.DataFrame(rows).fillna("")
    df.attrs["campos_tecnicos"] = [
        "MATNR", "BWKEY", "BKLAS", "VPRSV", "WAERS", "VERPR", "STPRS", "PEINH"
    ]
    return df
