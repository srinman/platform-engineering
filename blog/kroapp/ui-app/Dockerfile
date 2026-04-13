FROM python:3.12-slim

# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Bundle Bootstrap 5.3.3 locally — no CDN dependency at runtime
RUN mkdir -p static && \
    apt-get update -qq && apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -fsSL "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" \
         -o static/bootstrap.min.css && \
    curl -fsSL "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" \
         -o static/bootstrap.bundle.min.js && \
    apt-get purge -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
