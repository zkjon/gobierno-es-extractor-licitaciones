"""
Aplicación para automatizar la navegación click por click en la página
de contratación del estado español y extraer datos específicos.
"""

import time
from datetime import datetime

from navigator import ContratacionNavigator
from regions import select_region_url, get_all_regions, get_csv_filename
from processor import process_region
from utils import (
    setup_logging,
    restore_logging,
    print_header,
    print_info,
    print_success,
    print_error,
    print_warning,
    format_elapsed_time,
)


def main():
    """Función principal para ejecutar la navegación paso a paso."""
    
    # Configurar logging
    log_file, original_stdout, log_filename = setup_logging()
    navigator = None
    
    try:
        # Guardar tiempo de inicio
        start_time = datetime.now()
        
        print_header("EXTRACTOR DE LICITACIONES - CONTRATACIÓN DEL ESTADO")
        print_info(f"Inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print_info(f"Log guardado en: {log_filename}\n")
        
        # PASO 0: Seleccionar región y URL al inicio
        url_seleccionada, region_nombre = select_region_url()
        
        if not url_seleccionada:
            print_error("No se seleccionó ninguna región. Saliendo...")
            return
        
        # Crear instancia del navegador
        navigator = ContratacionNavigator(headless=False, slow_mo=500)
        
        # Iniciar navegador
        navigator.start()
        
        # Determinar qué regiones procesar
        if url_seleccionada == "TODAS":
            print_header("PROCESANDO TODAS LAS REGIONES")
            todas_las_regiones = get_all_regions()
            all_combined_data = []
            regiones_procesadas = 0
            
            for idx, region in enumerate(todas_las_regiones, 1):
                print(f"\n{'─'*70}")
                print_info(f"Región {idx}/{len(todas_las_regiones)}: {region['nombre']}")
                print(f"{'─'*70}")
                
                data_region = process_region(navigator, region['url'], region['nombre'])
                all_combined_data.extend(data_region)
                regiones_procesadas += 1
                
                if idx < len(todas_las_regiones):
                    print_info("Pausa antes de procesar la siguiente región...")
                    time.sleep(1)
            
            # Guardar todos los datos combinados
            if all_combined_data:
                filename = get_csv_filename("Todas")
                navigator.save_to_csv(all_combined_data, filename)
                print_header("PROCESO COMPLETADO")
                print_success(f"Total: {len(all_combined_data)} registros de {regiones_procesadas} región(es)")
                print_success(f"Archivo guardado: {filename}")
            else:
                print_warning("No se extrajeron datos de ninguna región")
        else:
            # Procesar una sola región
            all_extracted_data = process_region(navigator, url_seleccionada, region_nombre)
            
            # Guardar datos en CSV con nombre según la región
            if all_extracted_data:
                filename = get_csv_filename(region_nombre)
                navigator.save_to_csv(all_extracted_data, filename)
                print_header("PROCESO COMPLETADO")
                print_success(f"Total: {len(all_extracted_data)} registros extraídos")
                print_success(f"Archivo guardado: {filename}")
            else:
                print_warning("No se extrajeron datos")
        
        # Calcular y mostrar tiempo total transcurrido
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        elapsed_formatted = format_elapsed_time(elapsed_time)
        print_info(f"Fin: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print_info(f"Tiempo total transcurrido: {elapsed_formatted}")
        
    except KeyboardInterrupt:
        print_warning("\nProceso interrumpido por el usuario")
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if navigator:
            print("\n" + "─"*70)
            print_success("Cerrando navegador...")
            navigator.close()
        # Mostrar mensaje final antes de restaurar logging
        if log_file:
            print_info(f"Log guardado en: {log_filename}")
        # Restaurar logging y cerrar archivo
        restore_logging(log_file, original_stdout)


if __name__ == "__main__":
    main()
