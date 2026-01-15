"""
Funciones para manejo de regiones y URLs.
"""

from utils.printing import print_header, print_success, print_info, print_error, print_warning


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
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=IVv54tL29qQ%3D'
        },
        '2': {
            'nombre': 'Este',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=7QuTKak6qkc%3D'
        },
        '3': {
            'nombre': 'Oeste',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=uVw2GiaBY5s%3D'
        },
        '4': {
            'nombre': 'Centro',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=BxL%2BJUo%2Bqpg%3D'
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
                    print_info("Se procesarán todas las regiones (Sur, Este, Oeste, Centro)")
                print()
                return region['url'], region['nombre']
            else:
                print_error("Opción no válida. Por favor, selecciona un número del 1 al 5.")
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
        {'nombre': 'Sur', 'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=IVv54tL29qQ%3D'},
        {'nombre': 'Este', 'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=7QuTKak6qkc%3D'},
        {'nombre': 'Oeste', 'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=uVw2GiaBY5s%3D'},
        {'nombre': 'Centro', 'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=BxL%2BJUo%2Bqpg%3D'},
    ]


def get_csv_filename(region_nombre: str):
    """
    Genera el nombre del archivo CSV según la región.
    
    Args:
        region_nombre: Nombre de la región
    
    Returns:
        Nombre del archivo CSV
    """
    if region_nombre.lower() == "todas":
        return "todas_las_suministraciones.csv"
    else:
        return f"{region_nombre.lower()}_suministraciones.csv"
