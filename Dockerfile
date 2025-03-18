FROM ghcr.io/callmepk/python-poetry:3.10  # Готовый образ с Python 3.10 + poetry

WORKDIR /app
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "telegram_bot.py"]
