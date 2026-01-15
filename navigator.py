"""
Clase para navegar y extraer datos de la plataforma de contratación.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import csv
import json
from typing import Dict, Optional, List

from utils.printing import (
    print_info, print_success, print_error, print_warning
)


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
        print_info("Iniciando navegador...")
        try:
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
            print_success("Navegador iniciado (configurado en español de España)")
        except Exception as e:
            print_error(f"Error al iniciar el navegador: {str(e)}")
            raise
    
    def navigate_to_page(self):
        """Navega a la página inicial."""
        print_info(f"Navegando a la página...")
        try:
            self.page.goto(self.base_url, wait_until="networkidle", timeout=30000)
            time.sleep(1)  # Espera reducida
            print_success("Página cargada correctamente")
            return True
        except PlaywrightTimeoutError:
            print_error("Timeout al cargar la página (30 segundos)")
            return False
        except Exception as e:
            print_error(f"Error al navegar: {str(e)}")
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
            # Intentar diferentes métodos de selección
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            elif selector.startswith("text="):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            # Esperar a que el elemento sea visible y clickeable
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.click(timeout=timeout)
            
            time.sleep(0.5)  # Pausa reducida
            return True
            
        except PlaywrightTimeoutError:
            return False
        except Exception as e:
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
        print_info(f"Buscando: {description}")
        timeout_per_selector = max(3000, timeout // len(selectors))
        
        for i, selector in enumerate(selectors, 1):
            if self.click_element(selector, description, timeout=timeout_per_selector):
                print_success(f"Click en '{description}' realizado")
                return True
            time.sleep(0.2)  # Pausa reducida entre intentos
        
        print_error(f"No se encontró '{description}' después de {len(selectors)} intentos")
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
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.clear()
            element.fill(value)
            
            time.sleep(0.2)
            return True
            
        except PlaywrightTimeoutError:
            return False
        except Exception:
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
            if selector.startswith("//") or selector.startswith("(//"):
                element = self.page.locator(selector).first
            else:
                element = self.page.locator(selector).first
            
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            
            # Intentar múltiples estrategias de selección
            # Estrategia 1: Por value (más rápido y confiable)
            try:
                element.select_option(value=value, timeout=2000)
                time.sleep(0.2)
                return True
            except:
                pass
            
            # Estrategia 2: Por texto visible exacto (label)
            try:
                element.select_option(label=value, timeout=2000)
                time.sleep(0.2)
                return True
            except:
                pass
            
            # Estrategia 3: Buscar en todas las opciones
            try:
                options = element.locator("option").all()
                for option in options:
                    try:
                        option_text = option.inner_text(timeout=500).strip()
                        option_value = option.get_attribute("value") or ""
                        
                        if (value.lower() in option_text.lower() or 
                            option_text.lower() in value.lower() or
                            value == option_text or
                            value == option_value):
                            
                            if option_value:
                                element.select_option(value=option_value, timeout=2000)
                                time.sleep(0.2)
                                return True
                            
                            # Por índice
                            all_options = element.locator("option").all()
                            for idx, opt in enumerate(all_options):
                                if opt == option:
                                    element.select_option(index=idx, timeout=2000)
                                    time.sleep(0.2)
                                    return True
                    except:
                        continue
            except:
                pass
            
            return False
            
        except PlaywrightTimeoutError:
            return False
        except Exception:
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
        timeout_per_selector = max(3000, timeout // len(selectors))
        
        for selector in selectors:
            if self.fill_input(selector, value, description, timeout=timeout_per_selector):
                print_success(f"Campo '{description}' rellenado: {value}")
                return True
            time.sleep(0.2)
        
        print_error(f"No se pudo rellenar '{description}'")
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
        timeout_per_selector = max(3000, timeout // len(selectors))
        
        for selector in selectors:
            if self.select_option(selector, value, description, timeout=timeout_per_selector):
                print_success(f"'{description}' = '{value}'")
                return True
            time.sleep(0.2)
        
        print_error(f"No se pudo seleccionar '{value}' en '{description}'")
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
    
    def get_result_links(self):
        """
        Obtiene todos los enlaces de los resultados de búsqueda.
        Busca enlaces en la tabla de resultados que apuntan a detalle_licitacion.
        
        Returns:
            Lista de URLs de los enlaces encontrados
        """
        links = []
        try:
            # Buscar enlaces en la tabla de resultados
            link_elements = self.page.locator("//table[@id='tableLicitacionesPerfilContratante']//td[@class='tdExpediente']//a[@target='_blank']").all()
            
            for element in link_elements:
                try:
                    href = element.get_attribute("href")
                    if href and "detalle_licitacion" in href:
                        # Asegurar que la URL sea absoluta
                        if href.startswith("/"):
                            href = "https://contrataciondelestado.es" + href
                        elif not href.startswith("http"):
                            href = "https://contrataciondelestado.es" + href
                        if href not in links:
                            links.append(href)
                except:
                    continue
            
            # Método alternativo si no se encontraron
            if not links:
                all_links = self.page.locator("//a[contains(@href, 'detalle_licitacion') and contains(@href, 'idEvl=')]").all()
                for element in all_links:
                    try:
                        href = element.get_attribute("href")
                        if href and "detalle_licitacion" in href and "idEvl=" in href:
                            if href.startswith("/"):
                                href = "https://contrataciondelestado.es" + href
                            elif not href.startswith("http"):
                                href = "https://contrataciondelestado.es" + href
                            if href not in links:
                                links.append(href)
                    except:
                        continue
            
            return links
        except Exception as e:
            print_error(f"Error obteniendo enlaces: {str(e)}")
            return links
    
    def extract_detail_data(self):
        """
        Extrae los datos específicos de la página de detalle de una licitación.
        
        Returns:
            Diccionario con los datos extraídos
        """
        data = {
            "valor_estimado": "",
            "adjudicatario": "",
            "fecha_publicacion": "",
            "tipo_documento": ""
        }
        
        try:
            self.page.wait_for_load_state("networkidle", timeout=20000)
            time.sleep(0.5)
            
            # Extraer Valor estimado del contrato
            try:
                valor_element = self.page.locator("//span[contains(@id, 'text_ValorContrato')]").first
                if valor_element.is_visible(timeout=2000):
                    valor_text = valor_element.inner_text(timeout=1000).strip()
                    # Buscar "Euros" cerca
                    try:
                        parent = valor_element.locator("..")
                        euros = parent.locator("//span[contains(text(), 'Euros')]").first
                        if euros.is_visible(timeout=500):
                            valor_text += " " + euros.inner_text(timeout=500).strip()
                    except:
                        pass
                    data["valor_estimado"] = valor_text
            except:
                pass
            
            # Extraer Adjudicatario
            try:
                adjudicatario_element = self.page.locator("//span[contains(@id, 'text_Adjudicatario')]").first
                if adjudicatario_element.is_visible(timeout=2000):
                    data["adjudicatario"] = adjudicatario_element.inner_text(timeout=1000).strip()
            except:
                pass
            
            # Extraer Fecha y Tipo de documento de "Adjudicación"
            try:
                tabla_rows = self.page.locator("//table[@id='myTablaDetalleVISUOE']//tbody//tr").all()
                for row in tabla_rows:
                    try:
                        tipo_doc = row.locator("td[2]").first
                        if tipo_doc.is_visible(timeout=500):
                            tipo_text = tipo_doc.inner_text(timeout=500).strip()
                            if "Adjudicación" in tipo_text:
                                fecha_cell = row.locator("td[1]").first
                                if fecha_cell.is_visible(timeout=500):
                                    data["fecha_publicacion"] = fecha_cell.inner_text(timeout=500).strip()
                                data["tipo_documento"] = tipo_text
                                break
                    except:
                        continue
            except:
                pass
            
            return data
            
        except Exception as e:
            return data
    
    def save_to_csv(self, data_list: List[Dict], filename: str = "licitaciones.csv"):
        """
        Guarda los datos extraídos en un archivo CSV.
        
        Args:
            data_list: Lista de diccionarios con los datos a guardar
            filename: Nombre del archivo CSV
        """
        try:
            if not data_list:
                print_warning("No hay datos para guardar")
                return
            
            # Determinar las columnas según si hay datos de región o no
            fieldnames = ["url", "valor_estimado", "adjudicatario", "fecha_publicacion", "tipo_documento"]
            if any("region" in data for data in data_list):
                fieldnames.insert(1, "region")
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
            
            print_success(f"CSV guardado: {filename} ({len(data_list)} registros)")
        except Exception as e:
            print_error(f"Error guardando CSV: {str(e)}")
    
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
