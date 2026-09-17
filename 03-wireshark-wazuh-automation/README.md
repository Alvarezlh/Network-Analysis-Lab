# Wireshark to Wazuh Automation

Automatización de captura de tráfico de red y envío a Wazuh para análisis en tiempo real.

## 📋 Arquitectura

Windows PC (Tráfico de Red)
↓
Kali Linux (Captura + Scripts)
├── Wireshark (tshark) → PCAP
├── Exporta a JSON
├── Storage Manager (limpia disco)
└── Envía a Wazuh
↓
Wazuh Manager (192.168.0.28)
├── Analiza eventos
├── Crea alertas
└── Dashboard


## 🗄️ Estrategia de almacenamiento

- **Captura:** 1 hora máximo
- **JSON:** Comprimido (.gz)
- **Rotación:** Automática cada hora
- **Limpieza:** Borra después de enviar a Wazuh
- **Espacio usado:** ~10 MB/hora (después de compresión)

## 📁 Estructura

- `scripts/` - Python y bash scripts
- `config/` - Configuración Wazuh
- `docs/` - Guías de setup

## 🚀 Próximos pasos

1. Storage Manager (limitar disco)
2. Script Python (captura + JSON)
3. Integración Wazuh
4. Reglas de detección

