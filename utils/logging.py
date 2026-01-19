"""
Utilidades para logging y redirección de salida.
"""

import os
import sys
from datetime import datetime


class Tee:
    """
    Clase para redirigir la salida tanto a la consola como a un archivo.
    """
    def __init__(self, *files):
        self.files = files
    
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    
    def flush(self):
        for f in self.files:
            f.flush()


def setup_logging():
    """
    Configura el sistema de logging creando la carpeta logs y redirigiendo la salida.
    
    Returns:
        Tupla (log_file, original_stdout, log_filename) para poder restaurar al finalizar
    """
    # Crear carpeta logs si no existe
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Generar nombre del archivo con formato: log_YYYY-MM-DD_HH-MM-SS.log
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(logs_dir, f"log_{timestamp}.log")
    
    # Abrir archivo de log
    log_file = open(log_filename, 'w', encoding='utf-8')
    
    # Guardar stdout original
    original_stdout = sys.stdout
    
    # Redirigir stdout a consola y archivo
    sys.stdout = Tee(sys.stdout, log_file)
    
    return log_file, original_stdout, log_filename


def restore_logging(log_file, original_stdout):
    """
    Restaura la salida original y cierra el archivo de log.
    
    Args:
        log_file: Archivo de log abierto
        original_stdout: stdout original
    """
    sys.stdout = original_stdout
    if log_file:
        log_file.close()
