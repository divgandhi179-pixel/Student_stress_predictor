FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run gunicorn on the specified PORT environment variable (Render sets this dynamically, defaults to 10000)
CMD sh -c "gunicorn -b 0.0.0.0:${PORT:-10000} app:app"
