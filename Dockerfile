FROM python:3.13-slim

WORKDIR /app

# Instala uv
RUN pip install --upgrade pip && pip install uv

# Copia solo pyproject.toml (y opcionalmente uv.lock si lo tienes)
COPY pyproject.toml ./
# COPY uv.lock ./

# Copia el código fuente
COPY src/ ./src/
COPY config/ ./config/
COPY data/ ./data/

# Instala las dependencias del proyecto usando uv sync
RUN uv sync

# Expone los puertos necesarios
EXPOSE 8000 8501

# Copia el script de arranque
COPY scripts/run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Comando por defecto: ejecuta el script que lanza ambos servicios
CMD ["/app/run.sh"]