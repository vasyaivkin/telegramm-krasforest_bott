FROM python:3.10  # Откат до Python 3.10

# Устанавливаем системные библиотеки
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    cargo \
    rustc

WORKDIR /app
COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir aiohttp==3.8.5 && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "telegram_bot.py"]
