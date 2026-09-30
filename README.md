# Network Analysis Lab - Wazuh SIEM Automation

**Portfolio de Análisis de Seguridad de Red con Wireshark y Wazuh SIEM**

Laboratorio completo para captura, análisis e ingesta de tráfico de red en un SIEM empresarial.

---

## 📋 Descripción General

Este proyecto demuestra:
- **Captura de tráfico de red** con Wireshark/tshark
- **Análisis de endpoints** e identificación de patrones de comunicación
- **Automatización SIEM** mediante Python y API REST
- **Detección de amenazas** con reglas custom en Wazuh
- **Investigación de incidentes** estilo SOC

---

## 📁 Estructura del Proyecto

Network-Analysis-Lab/
├── 01-home-network-analysis/ # Caso 1: Análisis CDN Anthropic
│ ├── README.md
│ ├── analysis/
│ │ ├── ip-endpoints.md
│ │ └── incident-report.md
│ ├── captures/
│ │ └── wireshark-screenshot.png
│ └── whois/
│ └── 160.79.104.10.txt
│
├── 02-cloudflare-traffic-analysis/ # Caso 2: Análisis CDN Cloudflare
│ ├── README.md
│ ├── analysis/
│ │ ├── ip-endpoints.md
│ │ └── incident-report.md
│ ├── captures/
│ │ └── cloudflare-screenshot.png
│ └── whois/
│ └── 162.159.141.124.txt
│
├── 03-wireshark-wazuh-automation/ # Caso 3: Automatización Wazuh
│ ├── README.md
│ ├── scripts/
│ │ ├── wireshark_to_wazuh.py # Script de captura e ingesta
│ │ └── storage_manager.sh # Limpieza y rotación de logs
│ ├── config/
│ │ ├── config.env # Variables de entorno (no en GitHub)
│ │ ├── wazuh_rules.xml # Reglas de detección custom
│ │ └── log_rotation.conf
│ ├── docs/
│ │ ├── setup.md # Instrucciones de instalación
│ │ └── automation_guide.md
│ └── .gitignore
│
└── README.md (este archivo)


---

## 🎯 Casos Completados

### **Caso 1: Análisis CDN Anthropic (13-09-2026)**

**Objetivo:** Identificar y clasificar tráfico hacia servidores externos

**Hallazgos:**
- **IP:** 160.79.104.10 (Anthropic, San Francisco)
- **Tráfico:** 39.32% del ancho de banda (192.168.0.x)
- **Protocolo:** HTTPS (Puerto 443)
- **Clasificación:** ✅ **Falso Positivo** - Navegación a claude.ai

**Metodología:**
1. Captura de 60s en Wireshark
2. Análisis de endpoints de red
3. Consulta OSINT (AbuseIPDB, WHOIS)
4. Redacción de reporte de incidente

**Archivos:** `/01-home-network-analysis/`

---

### **Caso 2: Análisis CDN Cloudflare (14-09-2026)**

**Objetivo:** Detectar patrones de tráfico CDN y volumen de datos

**Hallazgos:**
- **IP:** 162.159.141.124 (Cloudflare Inc., AS13335)
- **Tráfico:** 60.62% del ancho de banda (1,704 paquetes)
- **Otros orígenes:** Meta (~8%), Google (~3%), Anthropic (4.59%)
- **Clasificación:** ✅ **Legítimo** - Web browsing mediante CDN

**Técnicas de Análisis:**
- Estadísticas de paquetes por IP
- Identificación de protocolos
- ASN lookup y geolocalización
- Timeline de eventos de red

**Archivos:** `/02-cloudflare-traffic-analysis/`

---

### **Caso 3: Automatización Wireshark → Wazuh (25-09-2026)**

**Objetivo:** Crear pipeline automatizado de ingesta de tráfico de red en SIEM

**Componentes:**

#### **Script Python (`wireshark_to_wazuh.py`)**

Flujo: Captura (tshark) → JSON → Parsing → API Wazuh → Dashboard


**Funcionalidades:**
- ✅ Captura 60 segundos de tráfico en eth0
- ✅ Exporta a JSON con tshark
- ✅ Parsea primeros 50 paquetes
- ✅ Autentica con API REST de Wazuh (Bearer token)
- ✅ Envía eventos a Wazuh Manager
- ✅ Manejo de errores y logging

**Ejemplo de evento generado:**
```json
{
  "event_type": "network_traffic",
  "src_ip": "192.168.0.20",
  "dst_ip": "162.159.141.124",
  "protocol": "HTTPS",
  "dst_port": "443",
  "frame_length": "1507",
  "timestamp": "2026-09-26T11:30:32.542643253Z"
}
```

#### **Reglas de Detección Wazuh (`wazuh_rules.xml`)**

| Rule ID | Nombre | Nivel | Descripción |
|---------|--------|-------|-------------|
| 100000 | Parent Rule | 0 | Evento base de tráfico de red |
| 100001 | Cloudflare CDN | 3 | Detecta tráfico a 162.159.141.124 |
| 100002 | Anthropic CDN | 3 | Detecta tráfico a 160.79.104.10 |
| 100003 | HTTPS Traffic | 2 | Detecta tráfico encriptado puerto 443 |
| 100004 | Network Analysis | 5 | Alerta general de análisis de tráfico |

**Archivos:** `/03-wireshark-wazuh-automation/`

---

## 🛠️ Configuración y Uso

### **Requisitos**
Kali Linux 2023.x+
Python 3.10+
Wireshark/tshark
Wazuh Manager 4.14.6+ (OVA en VirtualBox)
curl, git, nano

### **Instalación**

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Alvarezlh/Network-Analysis-Lab.git
cd Network-Analysis-Lab/03-wireshark-wazuh-automation
```

2. **Instalar dependencias Python:**
```bash
pip install requests python-dotenv
```

3. **Configurar variables de entorno:**
```bash
cp config/config.env.example config/config.env
nano config/config.env
```

**config.env:**

WAZUH_API_URL=https://192.168.0.20:55000
WAZUH_USER=wazuh
WAZUH_PASS=wazuh
CAPTURE_DURATION=60
CAPTURE_INTERFACE=eth0
LOG_DIR=/home/kali/wireshark_logs
RETENTION_DAYS=7


4. **Cargar reglas en Wazuh:**
   - Dashboard → Management → Rules → Custom rules
   - Crear: `0100-wireshark_network_analysis.xml`
   - Copiar contenido de `config/wazuh_rules.xml`
   - Save y reiniciar: `sudo systemctl restart wazuh-manager`

### **Ejecución**

```bash
cd scripts/
python3 wireshark_to_wazuh.py
```

**Output esperado:**
==================================================
🚀 Wireshark to Wazuh Automation
📡 Capturando 60s...
✅ Captura guardada (8248 paquetes)
📊 Analizando...
✅ 50 paquetes analizados
🔐 Autenticando en Wazuh...
✅ Autenticado
📤 Enviando 50 eventos...
✅ Enviado
🧹 Limpiando...
✅ Limpieza completa

✅ Proceso completado


### **Verificación en Dashboard**

1. Acceder: `https://192.168.0.20`
2. **Security Events** → Filtrar por `rule.id: 100001-100004`
3. Revisar eventos capturados y análisis

---

## 🐛 Problemas Conocidos

### **Problema 1: DHCP y cambio de IPs**

Síntoma: Las IPs de Kali y Wazuh cambian cada sesión
Solución: Ejecutar 'ip addr' antes de iniciar
Actualizar WAZUH_API_URL en config.env si cambió


### **Problema 2: IPv6 en lugar de IPv4**

Síntoma: Wazuh recibe dirección MAC/IPv6 en lugar de 192.168.x.x
Solución: Deshabilitar IPv6 en VirtualBox:
En VM Wazuh → sudo nano /etc/netplan/00-installer-config.yaml
Agregar: dhcp6: false
Luego: sudo netplan apply


### **Problema 3: Wazuh Dashboard no carga**

Síntoma: Pantalla en blanco después de iniciar
Solución: Esperar 10-15 minutos (OpenSearch es lento)
sudo systemctl restart elasticsearch wazuh-manager wazuh-dashboard
Limpiar caché del navegador (Ctrl + Shift + Delete)


### **Problema 4: API Wazuh rechaza eventos**

Síntoma: Status 401 o 403 en respuesta de API
Solución: Verificar credenciales en config.env
Reiniciar wazuh-manager: sudo systemctl restart wazuh-manager
Comprobar que JSON tiene estructura correcta


---

## 📊 Arquitectura SIEM

Kali Linux (192.168.0.15) Wazuh Manager (192.168.0.20)
┌─────────────────────┐ ┌──────────────────────┐
│ tshark (captura) │ │ Wazuh Manager │
│ Python (parseo) │────────→│ Elasticsearch │
│ API REST (envío) │ │ Wazuh Dashboard │
└─────────────────────┘ └──────────────────────┘
↓ ↓
wireshark_logs/ Security Events
(JSON temporales) (Visualización)


---

## 🔐 Seguridad y Privacidad

**Datos redactados antes de publicar:**
- SSID de red: `Home-Network` (no específico)
- IPs privadas: `192.168.0.x` (formato genérico)
- Nombres de host: No publicados

**Datos seguros de publicar:**
- IPs públicas: Cloudflare, Anthropic (ya públicas en WHOIS)
- Reglas de Wazuh: Métodos de detección
- Reportes de análisis: Metodología

---

## 📈 Skills Demostrados

✅ **Network Security**
- Captura y análisis de tráfico
- Identificación de endpoints y patrones
- OSINT e investigación de IPs

✅ **SIEM & Log Management**
- Ingesta de eventos en Wazuh
- Escritura de reglas de detección custom
- Análisis de Security Events

✅ **Automation & Scripting**
- Python con requests y subprocess
- Integración API REST
- Gestión de archivos y logging

✅ **Blue Team / SOC Analyst**
- Redacción de reportes de incidente
- Clasificación de alertas (True/False Positive)
- Remediación de falsos positivos

---

## 📚 Referencias

- [Wazuh Official Documentation](https://documentation.wazuh.com/)
- [Wireshark User Guide](https://www.wireshark.org/docs/)
- [AbuseIPDB](https://www.abuseipdb.com/)
- [WHOIS Lookup](https://www.whois.com/)

---

## 📝 Próximos Pasos

- [ ] Crear dashboard visual en Wazuh con gráficos de tráfico
- [ ] Implementar cron job para automatización horaria
- [ ] Agregar detección de anomalías (machine learning)
- [ ] Integración con Slack para alertas en tiempo real
- [ ] Documentar casos adicionales de análisis

---

## 👤 Autor

**Luis Enrique Alvarez Hernandez**
- Portfolio: SOC Analyst | Blue Team
- LinkedIn: [linkedin.com/in/luis-enrique-alvarez/](https://linkedin.com/in/luis-enrique-alvarez/)
- Ubicación: Barcelona, España

---

## 📄 Licencia

Este proyecto es de código abierto para propósitos educativos y de portfolio.

Última actualización: 30-09-2026
Estado: En desarrollo (v1.0)