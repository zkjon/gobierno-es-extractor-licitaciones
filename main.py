"""
Aplicación para automatizar la navegación click por click en la página
de contratación del estado español y extraer datos específicos.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import json
from typing import Dict, Optional


class ContratacionNavigator:
    """Clase para navegar y extraer datos de la plataforma de contratación."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 500):
        """
        Inicializa el navegador.
        
        Args:
            headless: Si True, el navegador se ejecuta en modo headless
            slow_mo: Milisegundos de pausa entre acciones (útil para debugging)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.base_url = None  # Se establecerá según la selección del usuario
        self.extracted_data = {}
    
    def start(self):
        """Inicia el navegador y la página."""
        print("🚀 Iniciando navegador...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        # Crear contexto con configuración en español de España
        self.context = self.browser.new_context(
            locale="es-ES",
            timezone_id="Europe/Madrid",
            viewport={"width": 1920, "height": 1080}
        )
        self.page = self.context.new_page()
        print("✅ Navegador iniciado correctamente (configurado en español de España)")
    
    def navigate_to_page(self):
        """Navega a la página inicial."""
        print(f"🌐 Navegando a: {self.base_url}")
        try:
            self.page.goto(self.base_url, wait_until="networkidle", timeout=30000)
            print("✅ Página cargada correctamente")
            # Esperar un momento para que la página se renderice completamente
            time.sleep(2)
            return True
        except PlaywrightTimeoutError:
            print("❌ Error: Timeout al cargar la página")
            return False
        except Exception as e:
            print(f"❌ Error al navegar: {str(e)}")
            return False
    
    def click_element(self, selector: str, description: str = "", timeout: int = 10000):
        """
        Hace click en un elemento de la página.
        
        Args:
            selector: Selector CSS, XPath o texto del elemento
            description: Descripción del elemento para logging
            timeout: Tiempo máximo de espera en milisegundos
        
        Returns:
            True si el click fue exitoso, False en caso contrario
        """
        try:
            print(f"🖱️  Haciendo click en: {description or selector}")
            
            # Intentar diferentes métodos de selección
            if selector.startswith("//") or selector.startswith("(//"):
                # XPath
                element = self.page.locator(selector).first
            elif selector.startswith("text="):
                # Selector de texto
                element = self.page.locator(selector).first
            else:
                # CSS selector
                element = self.page.locator(selector).first
            
            # Esperar a que el elemento sea visible y clickeable
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.click(timeout=timeout)
            
            print(f"✅ Click realizado correctamente")
            time.sleep(1)  # Pequeña pausa después del click
            return True
            
        except PlaywrightTimeoutError:
            print(f"❌ Error: No se encontró el elemento '{description or selector}' después de {timeout}ms")
            return False
        except Exception as e:
            print(f"❌ Error al hacer click: {str(e)}")
            return False
    
    def click_element_multiple_selectors(self, selectors: list, description: str = "", timeout: int = 15000):
        """
        Intenta hacer click usando múltiples selectores hasta que uno funcione.
        
        Args:
            selectors: Lista de selectores a intentar
            description: Descripción del elemento para logging
            timeout: Tiempo máximo de espera por selector en milisegundos
        
        Returns:
            True si algún click fue exitoso, False en caso contrario
        """
        print(f"🔍 Buscando elemento: {description}")
        for i, selector in enumerate(selectors, 1):
            print(f"   Intentando selector {i}/{len(selectors)}: {selector[:80]}...")
            if self.click_element(selector, description, timeout=timeout // len(selectors)):
                return True
            time.sleep(0.5)  # Pequeña pausa entre intentos
        
        print(f"❌ No se pudo encontrar el elemento '{description}' con ninguno de los selectores")
        return False
    
    def wait_for_element(self, selector: str, description: str = "", timeout: int = 10000):
        """
        Espera a que un elemento aparezca en la página.
        
        Args:
            selector: Selector del elemento
            description: Descripción del elemento para logging
            timeout: Tiempo máximo de espera en milisegundos
        
        Returns:
            True si el elemento apareció, False en caso contrario
        """
        try:
            print(f"⏳ Esperando elemento: {description or selector}")
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            element.wait_for(state="visible", timeout=timeout)
            print(f"✅ Elemento encontrado")
            return True
        except Exception as e:
            print(f"❌ Error esperando elemento: {str(e)}")
            return False
    
    def fill_input(self, selector: str, value: str, description: str = "", timeout: int = 10000):
        """
        Rellena un campo de texto (input o textarea).
        
        Args:
            selector: Selector del campo
            value: Valor a introducir
            description: Descripción del campo para logging
            timeout: Tiempo máximo de espera en milisegundos
        
        Returns:
            True si se rellenó correctamente, False en caso contrario
        """
        try:
            print(f"✏️  Rellenando campo '{description or selector}' con: {value}")
            
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.clear()
            element.fill(value)
            
            print(f"✅ Campo rellenado correctamente")
            time.sleep(0.5)
            return True
            
        except PlaywrightTimeoutError:
            print(f"❌ Error: No se encontró el campo '{description or selector}' después de {timeout}ms")
            return False
        except Exception as e:
            print(f"❌ Error rellenando campo: {str(e)}")
            return False
    
    def select_option(self, selector: str, value: str, description: str = "", timeout: int = 10000):
        """
        Selecciona una opción en un dropdown/select.
        
        Args:
            selector: Selector del elemento select
            value: Valor u opción a seleccionar (puede ser texto visible o value)
            description: Descripción del campo para logging
            timeout: Tiempo máximo de espera en milisegundos
        
        Returns:
            True si se seleccionó correctamente, False en caso contrario
        """
        try:
            print(f"📋 Seleccionando '{value}' en: {description or selector}")
            
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            
            # Intentar múltiples estrategias de selección
            # Estrategia 1: Por texto visible exacto (label)
            try:
                element.select_option(label=value, timeout=3000)
                print(f"✅ Opción seleccionada correctamente (por label exacto)")
                time.sleep(0.5)
                return True
            except:
                pass
            
            # Estrategia 2: Por value
            try:
                element.select_option(value=value, timeout=3000)
                print(f"✅ Opción seleccionada correctamente (por value)")
                time.sleep(0.5)
                return True
            except:
                pass
            
            # Estrategia 3: Buscar en todas las opciones por texto parcial o exacto
            try:
                options = element.locator("option").all()
                print(f"   🔍 Buscando entre {len(options)} opciones disponibles...")
                
                for option in options:
                    try:
                        option_text = option.inner_text(timeout=1000).strip()
                        option_value = option.get_attribute("value") or ""
                        
                        # Buscar coincidencia exacta o parcial
                        if (value.lower() in option_text.lower() or 
                            option_text.lower() in value.lower() or
                            value == option_text or
                            value == option_value):
                            
                            # Intentar seleccionar por value primero
                            if option_value:
                                try:
                                    element.select_option(value=option_value, timeout=3000)
                                    print(f"✅ Opción '{option_text}' seleccionada correctamente (encontrada por texto)")
                                    time.sleep(0.5)
                                    return True
                                except:
                                    pass
                            
                            # Si falla, intentar por índice
                            try:
                                # Obtener el índice de la opción
                                all_options = element.locator("option").all()
                                for idx, opt in enumerate(all_options):
                                    if opt == option:
                                        element.select_option(index=idx, timeout=3000)
                                        print(f"✅ Opción '{option_text}' seleccionada correctamente (por índice)")
                                        time.sleep(0.5)
                                        return True
                            except:
                                pass
                    except:
                        continue
            except Exception as e:
                print(f"   ⚠️  Error buscando opciones: {str(e)}")
            
            # Si llegamos aquí, no se pudo seleccionar
            print(f"❌ No se encontró la opción '{value}' en el select")
            return False
            
            return False
            
        except PlaywrightTimeoutError:
            print(f"❌ Error: No se encontró el select '{description or selector}' después de {timeout}ms")
            return False
        except Exception as e:
            print(f"❌ Error seleccionando opción: {str(e)}")
            return False
    
    def debug_list_form_elements(self):
        """Lista todos los elementos de formulario disponibles para debug."""
        print("\n🔍 Listando elementos del formulario disponibles...")
        try:
            # Listar todos los selects
            selects = self.page.locator("select").all()
            print(f"\n📋 Selects encontrados: {len(selects)}")
            for i, select in enumerate(selects[:10], 1):  # Mostrar solo los primeros 10
                try:
                    name = select.get_attribute("name") or select.get_attribute("id") or "sin nombre"
                    label_text = ""
                    try:
                        # Intentar encontrar el label asociado
                        select_id = select.get_attribute("id")
                        if select_id:
                            label = self.page.locator(f"label[for='{select_id}']").first
                            if label.is_visible(timeout=1000):
                                label_text = label.inner_text(timeout=1000).strip()
                    except:
                        pass
                    print(f"   {i}. Select: {name} | Label: {label_text}")
                except:
                    pass
            
            # Listar todos los textareas
            textareas = self.page.locator("textarea").all()
            print(f"\n📝 Textareas encontrados: {len(textareas)}")
            for i, textarea in enumerate(textareas[:10], 1):
                try:
                    name = textarea.get_attribute("name") or textarea.get_attribute("id") or "sin nombre"
                    label_text = ""
                    try:
                        textarea_id = textarea.get_attribute("id")
                        if textarea_id:
                            label = self.page.locator(f"label[for='{textarea_id}']").first
                            if label.is_visible(timeout=1000):
                                label_text = label.inner_text(timeout=1000).strip()
                    except:
                        pass
                    print(f"   {i}. Textarea: {name} | Label: {label_text}")
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Error al listar elementos: {str(e)}")
    
    def fill_input_multiple_selectors(self, selectors: list, value: str, description: str = "", timeout: int = 15000):
        """
        Intenta rellenar un campo usando múltiples selectores hasta que uno funcione.
        
        Args:
            selectors: Lista de selectores a intentar
            value: Valor a introducir
            description: Descripción del campo para logging
            timeout: Tiempo máximo de espera por selector en milisegundos
        
        Returns:
            True si se rellenó correctamente, False en caso contrario
        """
        print(f"🔍 Buscando campo: {description}")
        for i, selector in enumerate(selectors, 1):
            print(f"   Intentando selector {i}/{len(selectors)}: {selector[:80]}...")
            if self.fill_input(selector, value, description, timeout=timeout // len(selectors)):
                return True
            time.sleep(0.3)
        
        print(f"❌ No se pudo encontrar el campo '{description}' con ninguno de los selectores")
        return False
    
    def select_option_multiple_selectors(self, selectors: list, value: str, description: str = "", timeout: int = 15000):
        """
        Intenta seleccionar una opción usando múltiples selectores hasta que uno funcione.
        
        Args:
            selectors: Lista de selectores a intentar
            value: Valor u opción a seleccionar
            description: Descripción del campo para logging
            timeout: Tiempo máximo de espera por selector en milisegundos
        
        Returns:
            True si se seleccionó correctamente, False en caso contrario
        """
        print(f"🔍 Buscando select: {description}")
        for i, selector in enumerate(selectors, 1):
            print(f"   Intentando selector {i}/{len(selectors)}: {selector[:80]}...")
            if self.select_option(selector, value, description, timeout=timeout // len(selectors)):
                return True
            time.sleep(0.3)
        
        print(f"❌ No se pudo encontrar el select '{description}' con ninguno de los selectores")
        return False
    
    def extract_text(self, selector: str, description: str = "", save_key: Optional[str] = None):
        """
        Extrae el texto de un elemento.
        
        Args:
            selector: Selector del elemento
            description: Descripción del elemento para logging
            save_key: Clave para guardar el dato extraído en extracted_data
        
        Returns:
            El texto extraído o None si hay error
        """
        try:
            print(f"📝 Extrayendo texto de: {description or selector}")
            
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            text = element.inner_text(timeout=5000).strip()
            
            if save_key:
                self.extracted_data[save_key] = text
                print(f"✅ Texto extraído y guardado en '{save_key}': {text[:50]}...")
            else:
                print(f"✅ Texto extraído: {text[:50]}...")
            
            return text
            
        except Exception as e:
            print(f"❌ Error extrayendo texto: {str(e)}")
            return None
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """Toma una captura de pantalla de la página actual."""
        try:
            self.page.screenshot(path=filename)
            print(f"📸 Captura guardada: {filename}")
        except Exception as e:
            print(f"❌ Error al tomar captura: {str(e)}")
    
    def save_data(self, filename: str = "extracted_data.json"):
        """Guarda los datos extraídos en un archivo JSON."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_data, f, ensure_ascii=False, indent=2)
            print(f"💾 Datos guardados en: {filename}")
        except Exception as e:
            print(f"❌ Error al guardar datos: {str(e)}")
    
    def show_menu_and_select_region(self):
        """
        Muestra un menú interactivo para seleccionar una región.
        
        Returns:
            La opción seleccionada (1-4) o None si se cancela
        """
        print("\n" + "="*50)
        print("SELECCIONA UNA REGIÓN")
        print("="*50)
        print("\nOpciones disponibles:")
        print("  1. Sur")
        print("  2. Este")
        print("  3. Oeste")
        print("  4. Centro")
        print("\n" + "-"*50)
        
        while True:
            try:
                seleccion = input("Selecciona una opción (1-4): ").strip()
                
                if seleccion in ['1', '2', '3', '4']:
                    opciones = {
                        '1': 'Sur',
                        '2': 'Este',
                        '3': 'Oeste',
                        '4': 'Centro'
                    }
                    region_seleccionada = opciones[seleccion]
                    print(f"\n✅ Has seleccionado: {region_seleccionada}\n")
                    return region_seleccionada
                else:
                    print("❌ Opción no válida. Por favor, selecciona un número del 1 al 4.")
            except KeyboardInterrupt:
                print("\n⚠️  Selección cancelada por el usuario")
                return None
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                return None
    
    def click_region_link(self, region: str, timeout: int = 15000):
        """
        Hace click en el enlace correspondiente a la región seleccionada.
        
        Args:
            region: Nombre de la región (Norte, Sur, Este, Oeste, Centro)
            timeout: Tiempo máximo de espera en milisegundos
        
        Returns:
            True si el click fue exitoso, False en caso contrario
        """
        print(f"🔗 Buscando enlace para la región: {region}")
        
        # Crear múltiples selectores para encontrar el enlace de la región
        region_selectors = [
            f"//a[contains(text(), '{region}')]",
            f"//a[contains(., '{region}')]",
            f"//a[normalize-space()='{region}']",
            f"//a[contains(@href, '{region.lower()}')]",
            f"//a[contains(@title, '{region}')]",
            f"text={region}",
        ]
        
        return self.click_element_multiple_selectors(
            region_selectors,
            f"Enlace región {region}",
            timeout=timeout
        )
    
    def close(self):
        """Cierra el navegador y libera recursos."""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("🔒 Navegador cerrado")


def select_region_url():
    """
    Muestra un menú interactivo para seleccionar la región y devuelve la URL correspondiente.
    
    Returns:
        La URL correspondiente a la región seleccionada o None si se cancela
    """
    # URLs correspondientes a cada región
    urls_regiones = {
        '1': {
            'nombre': 'Sur',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=IVv54tL29qQ%3D'
        },
        '2': {
            'nombre': 'Este',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=7QuTKak6qkc%3D'  # URL actual (Este)
        },
        '3': {
            'nombre': 'Oeste',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=uVw2GiaBY5s%3D'
        },
        '4': {
            'nombre': 'Centro',
            'url': 'https://contrataciondelestado.es/wps/poc?uri=deeplink:perfilContratante&idBp=BxL%2BJUo%2Bqpg%3D'
        }
    }
    
    print("\n" + "="*50)
    print("SELECCIONA UNA REGIÓN")
    print("="*50)
    print("\nOpciones disponibles:")
    for key, value in urls_regiones.items():
        print(f"  {key}. {value['nombre']}")
    print("\n" + "-"*50)
    
    while True:
        try:
            seleccion = input("Selecciona una opción (1-5): ").strip()
            
            if seleccion in urls_regiones:
                region = urls_regiones[seleccion]
                print(f"\n✅ Has seleccionado: {region['nombre']}")
                print(f"📍 URL: {region['url']}\n")
                return region['url'], region['nombre']
            else:
                print("❌ Opción no válida. Por favor, selecciona un número del 1 al 5.")
        except KeyboardInterrupt:
            print("\n⚠️  Selección cancelada por el usuario")
            return None, None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None, None


def main():
    """Función principal para ejecutar la navegación paso a paso."""
    
    # PASO 0: Seleccionar región y URL al inicio
    print("\n" + "="*50)
    print("BIENVENIDO A LA APLICACIÓN DE NAVEGACIÓN")
    print("="*50)
    url_seleccionada, region_nombre = select_region_url()
    
    if not url_seleccionada:
        print("❌ No se seleccionó ninguna región. Saliendo...")
        return
    
    # Crear instancia del navegador
    # headless=False para ver el navegador, slow_mo=500 para ver las acciones más despacio
    navigator = ContratacionNavigator(headless=False, slow_mo=500)
    
    # Establecer la URL seleccionada
    navigator.base_url = url_seleccionada
    
    try:
        # Iniciar navegador
        navigator.start()
        
        # Navegar a la página inicial (con la URL seleccionada)
        if not navigator.navigate_to_page():
            print("❌ No se pudo cargar la página inicial")
            return
        
        # Tomar captura inicial
        navigator.take_screenshot("01_pagina_inicial.png")
        
        # ============================================
        # AQUÍ EMPIEZAN LOS CLICKS PASO A PASO
        # ============================================
        
        print("\n" + "="*50)
        print("INICIANDO NAVEGACIÓN CLICK POR CLICK")
        print("="*50 + "\n")
        
        # Esperar a que la página cargue completamente
        navigator.page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2)
        
        # Tomar captura de la página inicial (ya estamos en el perfil del contratante)
        navigator.take_screenshot("01_pagina_perfil_contratante.png")
        
        # PASO 1: Click en la pestaña "Licitaciones"
        licitaciones_selectors = [
            "//input[contains(@id, 'linkPrepLic')]",
            "//input[contains(@name, 'linkPrepLic')]",
            "//input[@type='submit' and @value='Licitaciones']",
            "//input[@title='Licitaciones']",
            "//input[contains(@id, 'linkPrepLic') or contains(@name, 'linkPrepLic')]",
            "//a[contains(text(), 'Licitaciones')]",
            "//button[contains(text(), 'Licitaciones')]",
            "//*[contains(@class, 'tab') and contains(., 'Licitaciones')]",
            "//*[contains(text(), 'Licitaciones') and (self::a or self::button or self::div)]",
            "text=Licitaciones",
            "//li[contains(., 'Licitaciones')]//a",
            "//nav//a[contains(., 'Licitaciones')]",
        ]
        
        if not navigator.click_element_multiple_selectors(
            licitaciones_selectors,
            "Pestaña Licitaciones",
            timeout=20000
        ):
            print("⚠️  No se pudo encontrar la pestaña Licitaciones. Tomando captura para debug...")
            navigator.take_screenshot("02_error_licitaciones.png")
            print("❌ No se puede continuar sin hacer click en Licitaciones")
            return
        
        # Esperar a que la nueva página/sección cargue
        print("⏳ Esperando a que cargue la sección de Licitaciones...")
        navigator.page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)  # Dar más tiempo para que aparezca el formulario
        
        # Tomar captura después del click en Licitaciones
        navigator.take_screenshot("02_despues_licitaciones.png")
        
        # PASO 2: Rellenar campos del formulario de búsqueda
        print("\n" + "-"*50)
        print("RELLENANDO CAMPOS DEL FORMULARIO")
        print("-"*50 + "\n")
        
        # Verificar que el formulario esté presente antes de intentar rellenarlo
        print("🔍 Verificando que el formulario esté presente...")
        formulario_encontrado = False
        formulario_selectors = [
            "//form",
            "//form[contains(., 'Búsqueda')]",
            "//form[contains(., 'procedimiento')]",
            "//*[contains(@class, 'form')]",
            "//*[contains(@id, 'form')]",
        ]
        
        for selector in formulario_selectors:
            try:
                element = navigator.page.locator(selector).first
                if element.is_visible(timeout=3000):
                    print(f"✅ Formulario encontrado con selector: {selector[:50]}...")
                    formulario_encontrado = True
                    break
            except:
                continue
        
        if not formulario_encontrado:
            print("⚠️  No se encontró el formulario. Tomando captura para debug...")
            navigator.take_screenshot("02_error_formulario_no_encontrado.png")
            print("⚠️  Listando elementos disponibles para debug...")
            navigator.debug_list_form_elements()
            print("⚠️  Continuando de todas formas...")
        
        # Esperar un poco para asegurar que los campos estén listos
        time.sleep(1)
        
        # Campo 1: Tipo de contrato = "Suministros" (valor="1")
        print("\n🔄 Rellenando: Tipo de contrato = 'Suministros'")
        tipo_contrato_selectors = [
            "//select[contains(@name, 'busReasProc07')]",
            "//select[contains(@id, 'busReasProc07')]",
            "//select[@title='Tipo de contrato']",
        ]
        navigator.select_option_multiple_selectors(
            tipo_contrato_selectors,
            "1",  # Valor para Suministros según el HTML
            "Tipo de contrato",
            timeout=8000
        )
        
        time.sleep(0.3)  # Pausa breve entre campos
        
        # Campo 2: Estado = "Resuelta" (valor="RES")
        print("\n🔄 Rellenando: Estado = 'Resuelta'")
        estado_selectors = [
            "//select[contains(@name, 'busReasProc11')]",
            "//select[contains(@id, 'busReasProc11')]",
            "//select[@title='Estado']",
        ]
        navigator.select_option_multiple_selectors(
            estado_selectors,
            "RES",  # Valor para Resuelta según el HTML
            "Estado",
            timeout=8000
        )
        
        time.sleep(0.3)  # Pausa breve entre campos
        
        # Campo 3: Objeto del contrato = "alimentación"
        print("\n🔄 Rellenando: Objeto del contrato = 'alimentación'")
        objeto_selectors = [
            "//textarea[contains(@name, 'busReasProc17')]",
            "//textarea[contains(@id, 'busReasProc17')]",
            "//textarea[@title='Objeto del contrato']",
        ]
        navigator.fill_input_multiple_selectors(
            objeto_selectors,
            "alimentación",
            "Objeto del contrato",
            timeout=8000
        )
        
        # Tomar captura después de rellenar los campos
        navigator.take_screenshot("03_formulario_rellenado.png")
        
        print("\n✅ Campos del formulario rellenados\n")
        
        # PASO 3: Click en el botón "Buscar"
        print("\n🔄 Haciendo click en el botón 'Buscar'...")
        buscar_selectors = [
            "//input[contains(@id, 'busReasProc18')]",
            "//input[contains(@name, 'busReasProc18')]",
            "//input[@type='submit' and @value='Buscar']",
            "//input[@title='Buscar']",
            "//input[@value='Buscar' and @type='submit']",
        ]
        
        if navigator.click_element_multiple_selectors(
            buscar_selectors,
            "Botón Buscar",
            timeout=10000
        ):
            # Esperar a que se procese la búsqueda
            print("⏳ Esperando a que se procesen los resultados de búsqueda...")
            navigator.page.wait_for_load_state("networkidle", timeout=30000)
            time.sleep(2)
            
            # Tomar captura después de la búsqueda
            navigator.take_screenshot("04_resultados_busqueda.png")
            print("✅ Búsqueda completada")
        else:
            print("⚠️  No se pudo hacer click en el botón Buscar")
            navigator.take_screenshot("04_error_buscar.png")
        
        # Continúa agregando pasos según necesites...
        
        print("\n" + "="*50)
        print("NAVEGACIÓN COMPLETADA")
        print("="*50 + "\n")
        
        # Guardar datos extraídos
        if navigator.extracted_data:
            navigator.save_data()
        
        # Tomar captura final
        navigator.take_screenshot("02_pagina_final.png")
        
        print("\n✅ Proceso completado exitosamente")
        
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Pulsar Enter para cerrar
        input("Presiona Enter para cerrar el navegador...")
        navigator.close()


if __name__ == "__main__":
    main()
