# многостадийная сборка в случае данного приложения малополезна
FROM python:3.14.5-slim

WORKDIR /app

COPY app.py .

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE ${BACKEND_PORT:-8080}

ENTRYPOINT ["python", "-u", "app.py"]
