# 📲 Envio_Masivo — WhatsApp Business API Sender

Herramienta de envío masivo de mensajes de WhatsApp desarrollada para apoyar la gestión de comunicaciones del área de **Gestión de las Artes** de la **Secretaría de Cultura de Cali**, Colombia.

---

## 📋 Descripción

Este proyecto permite enviar mensajes masivos a través de la **WhatsApp Business Cloud API (Meta)** usando plantillas de mensajes aprobadas. Está diseñado para notificar a participantes inscritos en programas culturales sobre talleres, eventos y actividades.

### Casos de uso
- Confirmaciones de asistencia a talleres
- Recordatorios de eventos culturales
- Envío de enlaces a formularios de inscripción
- Comunicación con semilleros artísticos y orquestas en ruta de fortalecimiento

---

## 🛠️ Tecnologías

- Python 3.11+
- [WhatsApp Business Cloud API (Meta)](https://developers.facebook.com/docs/whatsapp)
- Librería `requests`

---

## ⚙️ Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/Yacaicedo6/Envio_Masivo.git
cd Envio_Masivo
```

### 2. Instalar dependencias
```bash
pip install requests
```

### 3. Configurar credenciales
Edita el archivo `enviar_api.py` y completa:
```python
WA_ACCESS_TOKEN    = "tu_token_de_acceso"
WA_PHONE_NUMBER_ID = "tu_phone_number_id"
```

### 4. Preparar el CSV de contactos
Crea un archivo `numeros.csv` con este formato:
```
nombre,numero
Juan Pérez,3101234567
María López,3209876543
```

### 5. Configurar la plantilla
```python
TEMPLATE_NAME     = "nombre_de_tu_plantilla"
TEMPLATE_LANGUAGE = "es_CO"
CSV_FILE          = "numeros.csv"
```

---

## ▶️ Uso

```bash
python enviar_api.py
```

El script muestra el progreso en tiempo real y genera un reporte `reporte_envio.json` al finalizar.

---

## 📄 Reporte de envío

Al finalizar se genera automáticamente un archivo `reporte_envio.json`:
```json
{
  "enviados": ["3101234567", "3209876543"],
  "fallidos": [{"numero": "3001234567", "error": "..."}]
}
```

---

## 🔒 Seguridad

- Nunca subas tu `WA_ACCESS_TOKEN` al repositorio
- Usa variables de entorno o un archivo `.env` para las credenciales en producción
- Agrega `.env` y archivos CSV con datos personales al `.gitignore`

---

## 📁 Estructura del proyecto

```
Envio_Masivo/
├── enviar_api.py          # Script principal de envío
├── README.md              # Este archivo
├── .gitignore             # Archivos excluidos del repositorio
└── ejemplos/
    └── numeros_ejemplo.csv
```

---

## 👤 Autor

**Yan Caicedo**  
Contratista independiente — Gestión de las Artes  
Secretaría de Cultura de Cali, Colombia  
[github.com/Yacaicedo6](https://github.com/Yacaicedo6)

---

## 📜 Licencia

Uso interno. Todos los derechos reservados.
