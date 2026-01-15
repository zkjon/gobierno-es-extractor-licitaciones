# SAECO - Automatización de Navegación Web

Aplicación para automatizar la navegación click por click en la plataforma de contratación del estado español y extraer datos específicos.

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Instalar las dependencias de Python:**
```bash
pip install -r requirements.txt
```

2. **Instalar los navegadores de Playwright:**
```bash
playwright install chromium
```

## 📖 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Configuración

Puedes modificar el comportamiento del navegador editando la función `main()` en `main.py`:

- `headless=False`: Muestra el navegador (útil para debugging)
- `headless=True`: Ejecuta sin mostrar el navegador (más rápido)
- `slow_mo=500`: Añade una pausa de 500ms entre acciones (útil para ver qué está pasando)

### Agregar pasos de navegación

Para agregar clicks paso a paso, edita la función `main()` y agrega llamadas a `navigator.click_element()`:

```python
# Ejemplo de click por selector CSS
navigator.click_element("button#mi-boton", "Botón de inicio")

# Ejemplo de click por XPath
navigator.click_element("//button[contains(text(), 'Continuar')]", "Botón continuar")

# Ejemplo de click por texto
navigator.click_element("text=Iniciar sesión", "Enlace de login")
```

### Extraer datos

Para extraer texto de elementos:

```python
# Extraer y guardar en el diccionario de datos
navigator.extract_text("div#mi-campo", "Campo de datos", save_key="campo_1")

# Solo extraer sin guardar
texto = navigator.extract_text("div#mi-campo", "Campo de datos")
```

Los datos extraídos se guardan automáticamente en `extracted_data.json` al finalizar.

## 🛠️ Funcionalidades

- ✅ Navegación automatizada click por click
- ✅ Extracción de texto de elementos específicos
- ✅ Capturas de pantalla automáticas
- ✅ Espera inteligente de elementos
- ✅ Manejo de errores y timeouts
- ✅ Guardado de datos en JSON

## 📝 Estructura del Proyecto

```
SAECO/
├── main.py              # Script principal con la lógica de navegación
├── requirements.txt     # Dependencias de Python
├── README.md           # Este archivo
├── extracted_data.json # Datos extraídos (se genera automáticamente)
└── *.png              # Capturas de pantalla (se generan automáticamente)
```

## 🔍 Encontrar selectores

Para encontrar los selectores de los elementos que quieres clickear:

1. Abre la página en tu navegador
2. Haz click derecho en el elemento → "Inspeccionar"
3. En el código HTML, haz click derecho en el elemento → "Copy" → "Copy selector" (para CSS) o "Copy XPath"

## ⚠️ Notas

- La aplicación espera automáticamente a que los elementos sean visibles antes de interactuar con ellos
- Si un elemento no se encuentra, la aplicación mostrará un error y continuará
- Las capturas de pantalla se guardan automáticamente en cada paso importante
- Los datos extraídos se guardan en formato JSON con codificación UTF-8

## 🐛 Solución de problemas

**Error: "playwright not found"**
- Ejecuta: `playwright install chromium`

**Error: "Timeout waiting for element"**
- Aumenta el valor de `timeout` en la llamada a `click_element()` o `wait_for_element()`
- Verifica que el selector sea correcto

**La página no carga**
- Verifica tu conexión a internet
- Comprueba que la URL sea accesible
