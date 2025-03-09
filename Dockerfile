# Используем официальный образ Python
FROM python:3.12

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем проект
COPY . .

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]