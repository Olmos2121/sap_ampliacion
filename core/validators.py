from core.state import get_val


def validar(n: int, flujo: str, cfg: dict) -> tuple[list, list]:
    """
    Retorna (errores, avisos).
    Errores bloquean la generación.
    Avisos permiten generar con advertencia.
    """
    errores = []
    avisos  = []

    if n == 0:
        return ["No hay materiales cargados."], []

    # MATNR siempre requerido
    for i in range(n):
        if not str(get_val("MATNR", i, "")).strip():
            errores.append(f"Fila {i+1}: MATNR vacío.")

    # Descripción requerida en todos los flujos excepto sucursales
    if flujo != "Ampliación sucursales":
        for i in range(n):
            if not str(get_val("MAKTX", i, "")).strip():
                errores.append(f"Fila {i+1}: Descripción (MAKTX) vacía.")

    # Campos opcionales con aviso para centros logísticos
    if flujo == "Ampliación centros logísticos":
        for i in range(n):
            if not str(get_val("MATKL", i, "")).strip():
                avisos.append(f"Fila {i+1}: Grupo de productos (MATKL) vacío.")
            if not str(get_val("PRDHA", i, "")).strip():
                avisos.append(f"Fila {i+1}: Jerarquía de productos (PRDHA) vacía.")
            if cfg.get("VOLEH") and not str(get_val("VOLUM", i, "")).strip():
                avisos.append(f"Fila {i+1}: Volumen (VOLUM) vacío.")

    return errores, avisos
