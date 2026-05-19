def tabs_para_flujo(flujo: str, cfg: dict) -> list[str]:
    """
    Retorna la lista de nombres de tabs que deben mostrarse
    según el flujo y la configuración del tipo de material.
    """

    if flujo == "Ampliación centros logísticos":
        t = ["Datos básicos", "Datos de centro"]
        if cfg.get("CL_cadenas"):     t.append("Cadenas de distribución")
        if cfg.get("CL_fiscal"):      t.append("Clasificación fiscal")
        if cfg.get("CL_prevision"):   t.append("Datos de previsión")
        if cfg.get("CL_lugares"):     t.append("Lugares de almacenamiento")
        if cfg.get("CL_area_planif"): t.append("Área planif. MRP")
        if cfg.get("CL_valoracion"):  t.append("Datos de valoración")
        return t

    if flujo == "Ampliación sucursales":
        t = ["Datos básicos", "Datos de centro"]
        if cfg.get("SUC_valoracion"): t.append("Datos de valoración")
        return t

    if flujo == "Modificación datos básicos":
        return ["Datos básicos"]

    return ["Datos básicos"]
