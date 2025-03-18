FROM python:3.12

RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "telegram_bot.py"]
