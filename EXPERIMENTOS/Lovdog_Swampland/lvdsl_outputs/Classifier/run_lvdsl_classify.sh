#!/usr/bin/env bash

# Configuración de rutas
PYTHON_SCRIPT="lvdsl_reduc_dimension.py"
SENDER_BIN="/media/hataraku_wulfus/oShigoto/correo_sender"
#SENDER_BIN="$HOME/Documentos/oShigoto/correo_sender"
#HTML_OUTPUT="/tmp/lvdsl_reduc_dim.html"
HTML_OUTPUT="lvdsl_classify_grid/lvdsl_classify_report.html"
LOG_ERROR="/tmp/lvdsl_execution_error.log"
VENV_PATH=../../../venv
SEND_MAIL=true

# Limpieza inicial de reportes previos para evitar falsos positivos
rm -f "$HTML_OUTPUT" "$LOG_ERROR"

echo "[INFO] Iniciando ejecución de $PYTHON_SCRIPT..."

# Verificar que se está dentro de un entorno venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "[ALERTA] No se encuentra un entorno venv activo."
    echo "[INFO] Intentando activar el entorno venv..."
    if [ $VENV_PATH ]; then
        . "$VENV_PATH/bin/activate"
        echo "[OK] Entorno venv activado. Procediendo con la ejecución..."
    else
        echo "[ERROR] El entorno venv no pudo ser activado."
        exit 1
    fi
fi

# Ejecución capturando stderr en el archivo de log de errores
if python "$PYTHON_SCRIPT" 2> "$LOG_ERROR"; then
    if [ -f "$HTML_OUTPUT" ]; then
        echo "[OK] Proceso completado. Enviando reporte HTML..."
        "$SENDER_BIN" "LVDSL - Reporte de Reducción Dimensional" "$HTML_OUTPUT"
    else
        echo "[ALERTA] El script finalizó con código 0 pero no generó $HTML_OUTPUT"
        echo "Verifica que la función generate_classification_html haya sido llamada." > "$LOG_ERROR"
        "$SENDER_BIN" "LVDSL - Error: Reporte HTML no generado" "$LOG_ERROR"
    fi
else
    echo "[ERROR] Falló la ejecución del script Python."
    
    # Si el archivo de error quedó vacío por alguna razón, escribir un mensaje por defecto
    if [ ! -s "$LOG_ERROR" ]; then
        echo "Ocurrió un error desconocido durante la ejecución de $PYTHON_SCRIPT." > "$LOG_ERROR"
    fi

    if $SEND_MAIL; then
        echo "[INFO] Enviando bitácora de error por correo..."
        "$SENDER_BIN" "LVDSL - [FALLO] Error en ejecución del experimento" "$LOG_ERROR"
    fi
    exit 1
fi
