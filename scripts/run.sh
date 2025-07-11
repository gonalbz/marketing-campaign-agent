#!/bin/bash

# Lanza FastAPI en background usando uv run
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Espera un poco para que arranque FastAPI
sleep 2

# Lanza Streamlit en background usando uv run
uv run streamlit run src/frontend/app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

# Manejo de señales para terminar ambos procesos
trap "kill $FASTAPI_PID $STREAMLIT_PID 2>/dev/null; exit 0" SIGINT SIGTERM

echo "Servicios corriendo en:"
echo "  FastAPI:   http://localhost:8000"
echo "  Streamlit: http://localhost:8501"
echo "Presiona Ctrl+C para detener."

# Espera a que terminen los procesos
wait $FASTAPI_PID $STREAMLIT_PID