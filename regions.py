"""
Funciones para manejo de regiones y URLs.
"""

import os
from datetime import datetime

from utils.printing import (
    print_header, print_success, print_info, print_error, print_warning
)


def select_region_url():
    """
    Muestra un menú interactivo para seleccionar la región y devuelve la URL correspondiente.
    
    Returns:
        Tupla (url, nombre_region) o ("TODAS", "Todas") si se selecciona todas las regiones
        (None, None) si se cancela
    """
    # URLs correspondientes a cada región
    urls_regiones = {
        '1': {
            'nombre': 'Sur',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=IVv54tL29qQ%3D'
            )
        },
        '2': {
            'nombre': 'Este',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=7QuTKak6qkc%3D'
            )
        },
        '3': {
            'nombre': 'Oeste',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=uVw2GiaBY5s%3D'
            )
        },
        '4': {
            'nombre': 'Centro',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=BxL%2BJUo%2Bqpg%3D'
            )
        },
        '5': {
            'nombre': 'Todas',
            'url': 'TODAS'  # Indicador especial
        }
    }
    
    print_header("SELECCIÓN DE REGIÓN")
    print("\nOpciones disponibles:")
    for key, value in urls_regiones.items():
        print(f"  {key}. {value['nombre']}")
    print()

    while True:
        try:
            seleccion = input("👉 Selecciona una opción (1-5): ").strip()

            if seleccion in urls_regiones:
                region = urls_regiones[seleccion]
                print_success(f"Región seleccionada: {region['nombre']}")
                if region['url'] != 'TODAS':
                    print_info(f"URL: {region['url']}")
                else:
                    print_info(
                        "Se procesarán todas las regiones "
                        "(Sur, Este, Oeste, Centro)"
                    )
                print()
                return region['url'], region['nombre']
            print_error(
                "Opción no válida. Por favor, selecciona un número del 1 al 5."
            )
        except KeyboardInterrupt:
            print_warning("\nSelección cancelada por el usuario")
            return None, None
        except Exception as e:
            print_error(f"Error: {str(e)}")
            return None, None


def get_all_regions():
    """
    Devuelve todas las regiones disponibles con sus URLs.

    Returns:
        Lista de diccionarios con nombre y url de cada región
    """
    return [
        {
            'nombre': 'Sur',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=IVv54tL29qQ%3D'
            )
        },
        {
            'nombre': 'Este',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=7QuTKak6qkc%3D'
            )
        },
        {
            'nombre': 'Oeste',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=uVw2GiaBY5s%3D'
            )
        },
        {
            'nombre': 'Centro',
            'url': (
                'https://contrataciondelestado.es/wps/poc?uri=deeplink:'
                'perfilContratante&idBp=BxL%2BJUo%2Bqpg%3D'
            )
        },
    ]


def get_csv_filename(region_nombre: str, palabra_clave: str):
    """
    Genera el nombre del archivo CSV según la región y palabra clave.

    Args:
        region_nombre: Nombre de la región
        palabra_clave: Palabra clave usada para filtrar las búsquedas

    Returns:
        Ruta completa del archivo CSV en formato:
        suministrations/[region]/[palabra_clave]/export_YYYY-MM-DD_HH-MM-SS.csv
    """
    # Normalizar nombre de región para la carpeta
    region_folder = region_nombre.lower()
    if region_folder == "todas":
        region_folder = "todas"

    # Normalizar palabra clave para la carpeta (eliminar caracteres especiales)
    palabra_clave_folder = palabra_clave.lower().strip()
    # Reemplazar espacios y caracteres no válidos para nombres de carpeta
    palabra_clave_folder = "".join(
        c if c.isalnum() or c in ('-', '_') else '_'
        for c in palabra_clave_folder
    )

    # Crear estructura de carpetas: suministrations/[region]/[palabra_clave]/
    output_dir = os.path.join(
        "suministrations", region_folder, palabra_clave_folder
    )
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generar timestamp en formato YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Generar nombre del archivo con timestamp
    filename = f"export_{timestamp}.csv"

    # Devolver ruta completa
    return os.path.join(output_dir, filename)
