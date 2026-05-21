def tabs_para_flujo(flujo: str, cfg: dict, centros: list = None) -> list[str]:
    centros = centros or []

    if flujo == "Ampliación centros logísticos":
        t = ["Datos básicos", "Datos de centro"]
        if cfg.get("CL_cadenas"):     t.append("Cadenas de distribución")
        if cfg.get("CL_fiscal"):      t.append("Clasificación fiscal")
        # Previsión y Área MRP solo si A130 está seleccionado
        if cfg.get("CL_prevision")   and "A130" in centros: t.append("Datos de previsión")
        if cfg.get("CL_lugares"):     t.append("Lugares de almacenamiento")
        if cfg.get("CL_area_planif") and "A130" in centros: t.append("Área planif. MRP")
        if cfg.get("CL_valoracion"):  t.append("Datos de valoración")
        return t

    if flujo == "Ampliación sucursales":
        t = ["Datos básicos", "Datos de centro"]
        if cfg.get("SUC_valoracion"): t.append("Datos de valoración")
        return t

    if flujo == "Modificación datos básicos":
        return ["Datos básicos"]

    return ["Datos básicos"]