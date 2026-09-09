#!/usr/bin/env bash

# Configuraciones principales
SENDER_BIN="/media/hataraku_wulfus/oShigoto/correo_sender"  # Ajusta la ruta a tu binario/script emisor
SLEEP_INTERVAL=60           # Tiempo de espera entre comprobaciones (segundos)
BASE_DIR="."                # Directorio base de búsqueda

# Patrón del reporte HTML esperado para XGBoost
PATTERN="lvdsl_classify_report__XGBoost.html"

echo "[*] Iniciando demonio de monitoreo para el reporte HTML de XGBoost..."

while true; do
    # Búsqueda usando wildcards / find en el árbol de directorios
    HTML_OUTPUT=$(find "$BASE_DIR" -type f -name "$PATTERN" | head -n 1)

    if [[ -n "$HTML_OUTPUT" && -f "$HTML_OUTPUT" ]]; then
        echo "[+] Archivo detectado: $HTML_OUTPUT"
        
        # Tiempo de gracia previo al envío para asegurar que la escritura en disco haya finalizado
        echo "[*] Esperando 10 segundos adicionales para estabilizar la escritura del archivo..."
        sleep 10

        echo "[*] Enviando correo electrónico..."
        "$SENDER_BIN" "LVDSL - Reporte de Reducción Dimensional" "$HTML_OUTPUT"
        
        if [[ $? -eq 0 ]]; then
            echo "[OK] Notificación enviada exitosamente. Finalizando monitoreo."
            exit 0
        else
            echo "[!] Error al ejecutar el script emisor. Reintentando en el siguiente ciclo..."
        fi
    fi

    # Pausa antes de la siguiente verificación
    sleep "$SLEEP_INTERVAL"
done
