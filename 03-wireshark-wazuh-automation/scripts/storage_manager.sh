#!/bin/bash
# Storage Manager - Limpia y comprime logs

LOG_DIR="/home/kali/wireshark_logs"
MAX_SIZE_GB=2
ARCHIVE_DIR="$LOG_DIR/archive"

# Crear directorios
mkdir -p "$LOG_DIR" "$ARCHIVE_DIR"

# Comprimir archivos JSON
compress_logs() {
    echo "📦 Comprimiendo logs..."
    find "$LOG_DIR" -name "*.json" -not -path "*/archive/*" -exec gzip {} \;
    echo "✅ Logs comprimidos"
}

# Limpiar archivos antiguos (>7 días)
cleanup_old() {
    echo "🧹 Limpiando archivos antiguos..."
    find "$LOG_DIR" -name "*.json.gz" -mtime +7 -delete
    find "$LOG_DIR" -name "*.pcap" -mtime +1 -delete
    echo "✅ Limpieza completada"
}

# Monitorear espacio
check_space() {
    USED=$(du -sh "$LOG_DIR" | cut -f1)
    echo "💾 Espacio usado: $USED"
}

# Ejecutar todas las funciones
compress_logs
cleanup_old
check_space