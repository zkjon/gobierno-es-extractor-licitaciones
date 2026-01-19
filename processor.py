"""
Funciones para procesar regiones y extraer datos.
"""

import time
from typing import List, Dict

from navigator import ContratacionNavigator
from utils.printing import (
    print_header, print_step, print_info, print_success, 
    print_error, print_warning, print_progress
)


def process_region(navigator: ContratacionNavigator, url: str, region_nombre: str, palabra_clave: str):
    """
    Procesa una región completa: navega, rellena formulario, busca y extrae datos.
    
    Args:
        navigator: Instancia del navegador
        url: URL de la región a procesar
        region_nombre: Nombre de la región
        palabra_clave: Palabra clave para filtrar las búsquedas
    
    Returns:
        Lista de diccionarios con los datos extraídos
    """
    print_header(f"PROCESANDO REGIÓN: {region_nombre.upper()}")
    
    # Establecer la URL
    navigator.base_url = url
    
    # Navegar a la página inicial
    print_step(1, 4, f"Navegando a la página de {region_nombre}")
    if not navigator.navigate_to_page():
        print_error(f"No se pudo cargar la página para {region_nombre}")
        return []
    
    # PASO 1: Click en la pestaña "Licitaciones"
    print_step(2, 4, "Accediendo a la sección de Licitaciones")
    licitaciones_selectors = [
        "//input[contains(@id, 'linkPrepLic')]",
        "//input[contains(@name, 'linkPrepLic')]",
        "//input[@type='submit' and @value='Licitaciones']",
        "//input[@title='Licitaciones']",
    ]
    
    if not navigator.click_element_multiple_selectors(
        licitaciones_selectors,
        "Pestaña Licitaciones",
        timeout=20000
    ):
        print_error(f"No se pudo encontrar la pestaña Licitaciones para {region_nombre}")
        return []
    
    navigator.page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    
    # PASO 2: Rellenar campo de búsqueda con palabra clave
    print_step(3, 4, "Rellenando formulario de búsqueda")
    print_info(f"Configurando filtro: Objeto={palabra_clave}")
    
    objeto_selectors = [
        "//textarea[contains(@name, 'busReasProc17')]",
        "//textarea[contains(@id, 'busReasProc17')]",
        "//textarea[@title='Objeto del contrato']",
    ]
    navigator.fill_input_multiple_selectors(
        objeto_selectors,
        palabra_clave,
        "Objeto del contrato",
        timeout=8000
    )
    
    # PASO 3: Click en el botón "Buscar"
    buscar_selectors = [
        "//input[contains(@id, 'busReasProc18')]",
        "//input[contains(@name, 'busReasProc18')]",
        "//input[@type='submit' and @value='Buscar']",
    ]
    
    if not navigator.click_element_multiple_selectors(
        buscar_selectors,
        "Botón Buscar",
        timeout=10000
    ):
        print_error(f"No se pudo hacer click en Buscar para {region_nombre}")
        return []
    
    navigator.page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(1.5)
    
    # PASO 4: Extraer datos de todos los enlaces
    print_step(4, 4, "Extrayendo datos de los resultados")
    all_extracted_data = []
    page_num = 1
    total_processed = 0
    
    while True:
        links = navigator.get_result_links()
        
        if not links:
            if page_num == 1:
                print_warning("No se encontraron resultados")
            break
        
        print_info(f"Página {page_num}: {len(links)} licitaciones encontradas")
        
        for i, link in enumerate(links, 1):
            print_progress(i, len(links), f"Página {page_num}")
            
            try:
                original_page = navigator.page
                new_page = navigator.context.new_page()
                navigator.page = new_page
                new_page.goto(link, wait_until="networkidle", timeout=25000)
                time.sleep(0.5)
                
                data = navigator.extract_detail_data()
                data["url"] = link
                data["region"] = region_nombre
                all_extracted_data.append(data)
                total_processed += 1
                
                new_page.close()
                navigator.page = original_page
                time.sleep(0.2)
                
            except Exception as e:
                print_warning(f"Error procesando licitación: {str(e)[:40]}")
                try:
                    new_page.close()
                    navigator.page = original_page
                except:
                    pass
                continue
        
        # Verificar siguiente página
        try:
            siguiente_selectors = [
                "//input[@id='viewns_Z7_AVEQAI930GRPE02BR764FO30G0_:form1:siguienteLink']",
                "//input[@name='viewns_Z7_AVEQAI930GRPE02BR764FO30G0_:form1:siguienteLink']",
                "//input[@type='submit' and contains(@value, 'Siguiente')]",
            ]
            
            siguiente_encontrado = False
            for selector in siguiente_selectors:
                try:
                    siguiente_button = navigator.page.locator(selector).first
                    if siguiente_button.is_visible(timeout=2000) and siguiente_button.is_enabled():
                        siguiente_button.click()
                        navigator.page.wait_for_load_state("networkidle", timeout=30000)
                        time.sleep(1.5)
                        page_num += 1
                        siguiente_encontrado = True
                        break
                except:
                    continue
            
            if not siguiente_encontrado:
                break
        except:
            break
    
    print_success(f"{region_nombre}: {total_processed} registros extraídos de {page_num} página(s)")
    return all_extracted_data
