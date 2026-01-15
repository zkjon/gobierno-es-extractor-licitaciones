# Extractor de Suministraciones Alimentarias - Ministerio de Defensa

Aplicación automatizada para extraer información de licitaciones de suministros de alimentación desde los perfiles de contratante del **Ministerio de Defensa - Ejército de Tierra** en la plataforma oficial de contratación del estado español (contrataciondelestado.es).

## 📋 Descripción

Esta herramienta automatiza la extracción de datos de licitaciones públicas de suministros de alimentación. La aplicación:

- Navega automáticamente por la plataforma de contratación del estado
- Accede a los perfiles de contratante de 4 regiones del Ejército de Tierra (Sur, Este, Oeste, Centro)
- Rellena automáticamente formularios de búsqueda con filtros específicos:
  - Tipo de contrato: **Suministros**
  - Estado: **Resuelta**
  - Objeto: **alimentación**
- Extrae información de cada licitación encontrada
- Guarda los resultados en archivos CSV organizados por región con timestamps

## 🎯 Funcionalidades

- ✅ **Navegación automatizada**: Usa Playwright para simular interacciones del usuario
- ✅ **Búsqueda filtrada**: Busca automáticamente licitaciones de suministros de alimentación resueltas
- ✅ **Extracción de datos**: Obtiene información detallada de cada licitación
- ✅ **Múltiples regiones**: Procesa una región específica o todas las regiones disponibles
- ✅ **Organización de archivos**: Guarda resultados en `suministrations/[region]/export_YYYY-MM-DD_HH-MM-SS.csv`
- ✅ **Logging completo**: Registra todas las operaciones en archivos de log
- ✅ **Manejo de errores**: Continúa procesando aunque falle alguna licitación individual
- ✅ **Paginación automática**: Navega automáticamente por todas las páginas de resultados

## 📦 Prerequisitos

### 1. Python
- **Python 3.8 o superior** es requerido
- Descarga desde [python.org](https://www.python.org/downloads/)
- Verifica tu instalación: `python --version` o `python3 --version`

### 2. Chrome/Chromium
- **Google Chrome** o **Chromium** es necesario para Playwright
- Chrome normalmente viene preinstalado
- Si no lo tienes: [google.com/chrome](https://www.google.com/chrome/)

### 3. pip
- Normalmente viene incluido con Python
- Verifica con: `pip --version` o `pip3 --version`

## 🚀 Instalación

### Paso 1: Clonar o descargar el repositorio

```bash
git clone <url-del-repositorio>
cd SAECO
```

O descarga y extrae el código fuente.

### Paso 2: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

O si usas `pip3`:

```bash
pip3 install -r requirements.txt
```

### Paso 3: Instalar navegadores de Playwright

Playwright necesita descargar los binarios del navegador Chromium:

```bash
playwright install chromium
```

O si el comando anterior no funciona:

```bash
python -m playwright install chromium
```

## 📖 Uso

### Ejecutar la aplicación

```bash
python main.py
```

O si usas `python3`:

```bash
python3 main.py
```

### Flujo de trabajo

1. **Selección de región**: Al iniciar, se muestra un menú:
   - `1. Sur`
   - `2. Este`
   - `3. Oeste`
   - `4. Centro`
   - `5. Todas` (procesa todas las regiones)

2. **Navegación automática**: La aplicación:
   - Abre el navegador (visible por defecto)
   - Navega al perfil de contratante de la región seleccionada
   - Accede a la sección de Licitaciones
   - Rellena el formulario de búsqueda:
     - Tipo de contrato: Suministros
     - Estado: Resuelta
     - Objeto: alimentación
   - Ejecuta la búsqueda

3. **Extracción de datos**: Para cada licitación encontrada:
   - Abre la página de detalle en una nueva pestaña
   - Extrae los siguientes datos:
     - Valor estimado del contrato
     - Adjudicatario
     - Fecha de publicación
     - Tipo de documento
   - Cierra la pestaña y continúa con la siguiente

4. **Paginación**: Si hay más páginas de resultados, navega automáticamente a la siguiente

5. **Guardado de resultados**: Los datos se guardan en:
   - `suministrations/[region]/export_YYYY-MM-DD_HH-MM-SS.csv`
   - Ejemplo: `suministrations/sur/export_2026-01-15_16-11-30.csv`

6. **Logging**: Todas las operaciones se registran en:
   - `logs/log_YYYY-MM-DD_HH-MM-SS.txt`

### Configuración del navegador

Puedes modificar el comportamiento del navegador en `main.py` (línea ~47):

```python
navigator = ContratacionNavigator(headless=False, slow_mo=500)
```

- `headless=False`: Muestra el navegador (útil para ver el proceso)
- `headless=True`: Ejecuta sin mostrar el navegador (más rápido)
- `slow_mo=500`: Pausa de 500ms entre acciones (reduce a 0 para máxima velocidad)

## 📁 Estructura del Proyecto

```
SAECO/
├── main.py                 # Script principal - orquesta todo el proceso
├── navigator.py            # Clase ContratacionNavigator - maneja la navegación web
├── processor.py            # Funciones de procesamiento de regiones
├── regions.py              # Funciones de manejo de regiones y URLs
├── utils/                  # Paquete de utilidades
│   ├── __init__.py        # Exportaciones del paquete
│   ├── logging.py         # Utilidades de logging y redirección de salida
│   └── printing.py        # Utilidades de impresión formateada
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── suministrations/       # Carpeta de salida (se crea automáticamente)
│   ├── sur/              # Archivos CSV de la región Sur
│   ├── este/             # Archivos CSV de la región Este
│   ├── oeste/            # Archivos CSV de la región Oeste
│   ├── centro/           # Archivos CSV de la región Centro
│   └── todas/            # Archivos CSV cuando se procesan todas las regiones
└── logs/                  # Archivos de log (se crea automáticamente)
    └── log_*.txt         # Logs con timestamps
```

## 📊 Formato de Datos de Salida

Los archivos CSV contienen las siguientes columnas:

- `url`: URL completa de la licitación en contrataciondelestado.es
- `region`: Región de la licitación (Sur, Este, Oeste, Centro)
- `valor_estimado`: Valor estimado del contrato (ej: "145.899,91 Euros")
- `adjudicatario`: Empresa adjudicataria
- `fecha_publicacion`: Fecha de publicación de la adjudicación
- `tipo_documento`: Tipo de documento (normalmente "Adjudicación")

Los archivos se guardan con codificación UTF-8 con BOM para compatibilidad con Excel.

## 🛠️ Cómo Funciona

### Arquitectura Modular

La aplicación está organizada en módulos especializados:

1. **`main.py`**: Punto de entrada que orquesta todo el proceso
2. **`navigator.py`**: Clase `ContratacionNavigator` que encapsula la lógica de navegación web usando Playwright
3. **`processor.py`**: Contiene la función `process_region()` que procesa cada región
4. **`regions.py`**: Maneja la selección de regiones, URLs y generación de nombres de archivos
5. **`utils/`**: Utilidades reutilizables para logging e impresión formateada

### Proceso de Extracción

1. **Inicialización**: Se configura el logging y se inicia el navegador Chromium
2. **Selección**: El usuario selecciona la región a procesar
3. **Navegación**: Se navega a la URL del perfil de contratante de la región
4. **Acceso a Licitaciones**: Se hace click en la pestaña "Licitaciones"
5. **Búsqueda**: Se rellenan los filtros y se ejecuta la búsqueda:
   - Tipo de contrato: "1" (Suministros)
   - Estado: "RES" (Resuelta)
   - Objeto: "alimentación"
6. **Extracción**: Para cada resultado:
   - Se obtiene el enlace a la página de detalle
   - Se abre en una nueva pestaña
   - Se extraen los datos usando selectores XPath específicos
   - Se cierra la pestaña
7. **Paginación**: Si existe botón "Siguiente", se navega a la siguiente página
8. **Guardado**: Se guardan todos los datos en un archivo CSV con timestamp
9. **Finalización**: Se cierra el navegador y se restauran los logs

### Selectores Utilizados

La aplicación utiliza selectores XPath para encontrar elementos:

- **Pestaña Licitaciones**: `//input[contains(@id, 'linkPrepLic')]`
- **Tipo de contrato**: `//select[contains(@name, 'busReasProc07')]`
- **Estado**: `//select[contains(@name, 'busReasProc11')]`
- **Objeto**: `//textarea[contains(@name, 'busReasProc17')]`
- **Botón Buscar**: `//input[contains(@id, 'busReasProc18')]`
- **Enlaces de resultados**: `//table[@id='tableLicitacionesPerfilContratante']//td[@class='tdExpediente']//a[@target='_blank']`
- **Valor estimado**: `//span[contains(@id, 'text_ValorContrato')]`
- **Adjudicatario**: `//span[contains(@id, 'text_Adjudicatario')]`
- **Tabla de documentos**: `//table[@id='myTablaDetalleVISUOE']//tbody//tr`

## ⚠️ Notas Importantes

- La aplicación está diseñada específicamente para extraer información de suministraciones alimentarias de los perfiles de contratante del Ejército de Tierra
- La aplicación espera automáticamente a que los elementos sean visibles antes de interactuar
- Si un elemento no se encuentra, la aplicación mostrará un error pero continuará
- Los archivos CSV se guardan con codificación UTF-8 con BOM para compatibilidad con Excel
- Cada ejecución genera un nuevo archivo con timestamp, no sobrescribe archivos anteriores
- El proceso puede tardar varios minutos dependiendo del número de licitaciones encontradas
- Si la estructura de la página web cambia, los selectores pueden necesitar actualizarse

## 🐛 Solución de Problemas

### Error: "playwright not found" o "ModuleNotFoundError: No module named 'playwright'"
```bash
pip install -r requirements.txt
playwright install chromium
```

### Error: "Timeout waiting for element"
- La página puede estar cargando más lento de lo esperado
- Verifica tu conexión a internet
- Intenta ejecutar de nuevo
- La estructura de la página web puede haber cambiado

### Error: "Chrome/Chromium not found"
```bash
playwright install chromium
```

### La página no carga o hay errores de navegación
- Verifica tu conexión a internet
- Comprueba que la URL de contratación del estado sea accesible
- Intenta ejecutar con `headless=False` para ver qué está pasando

### Los archivos CSV están vacíos
- Verifica que haya licitaciones que cumplan los criterios de búsqueda
- Revisa los logs en la carpeta `logs/` para ver si hubo errores
- Los selectores pueden necesitar actualizarse si la página web ha cambiado

### No se encuentran licitaciones
- Verifica que existan licitaciones de suministros de alimentación resueltas en la región seleccionada
- Comprueba que los filtros de búsqueda sean correctos

## 📝 Dependencias

Las dependencias se encuentran en `requirements.txt`:

- `playwright==1.40.0`: Framework para automatización de navegadores
- `python-dotenv==1.0.0`: Manejo de variables de entorno (si se requiere en el futuro)

## 📝 Licencia

Este proyecto es de código abierto. Úsalo y modifícalo según tus necesidades.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras bugs o tienes sugerencias de mejora, no dudes en abrir un issue o crear un pull request.
