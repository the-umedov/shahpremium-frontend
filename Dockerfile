FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render/Railway $PORT orqali portni beradi — main.py buni o'qiydi.
CMD ["python", "main.py"]
