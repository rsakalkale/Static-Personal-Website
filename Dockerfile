# Stage 1: Build CSS using Node.js
FROM node:20-slim AS css-builder
WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY tailwind.config.js ./
COPY css/input.css ./css/
COPY templates/ ./templates/
RUN npm run build

# Stage 2: Production image using Python
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy the compiled CSS from Stage 1 into the static css folder
COPY --from=css-builder /build/css/main.css ./css/main.css

EXPOSE 8080

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} app:app"]
