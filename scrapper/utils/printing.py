"""
Utilidades para impresión formateada y mensajes.
"""


def print_header(text: str):
    """Imprime un encabezado formateado."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_step(step_num: int, total_steps: int, description: str):
    """Imprime un paso del proceso con formato."""
    print(f"\n[{step_num}/{total_steps}] {description}")
    print("-" * 70)


def print_success(message: str):
    """Imprime un mensaje de éxito."""
    print(f"✅ {message}")


def print_error(message: str):
    """Imprime un mensaje de error."""
    print(f"❌ {message}")


def print_warning(message: str):
    """Imprime un mensaje de advertencia."""
    print(f"⚠️  {message}")


def print_info(message: str):
    """Imprime un mensaje informativo."""
    print(f"ℹ️  {message}")


def format_elapsed_time(seconds: float) -> str:
    """
    Formatea el tiempo transcurrido en horas, minutos y segundos.
    
    Args:
        seconds: Tiempo en segundos (puede ser float)
    
    Returns:
        String formateado como "Xh Xm Xs" o "Xm Xs" o "Xs"
    """
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def print_progress(current: int, total: int, item: str = ""):
    """Imprime el progreso de una operación."""
    percentage = int((current / total) * 100) if total > 0 else 0
    bar_length = 40
    filled = int(bar_length * current / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\r  [{bar}] {percentage:3d}% ({current}/{total}) {item}", end="", flush=True)
    if current == total:
        print()  # Nueva línea al completar
