# Real-Time Cryptocurrency Price Tracker

Мониторинг цен криптовалют в реальном времени через WebSocket с интеграцией Binance, сохранением в PostgreSQL и REST API.

## 🌟 Особенности

- Подключение к Binance WebSocket API
- Сохранение данных в PostgreSQL
- REST API для доступа к историческим данным
- WebSocket-сервер для рассылки обновлений
- Контейнеризация с Docker и Docker Compose
- Настройка через переменные окружения (python-decouple)

## 🛠 Технологии

- **Backend**: Django 4.2, Django Channels
- **Базы данных**: PostgreSQL, Redis
- **Инфраструктура**: Docker, Docker Compose
- **Брокер сообщений**: Redis
- **Безопасность**: python-decouple для конфигурации

## 🚀 Быстрый старт

### Предварительные требования
- Docker 20.10+
- Docker Compose 2.0+

```bash
git clone git@github.com:ilg123/binance_monitor.git
```

### Создайте .env файл:
```bash
DB_NAME=crypto_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
```

### Запуск
```bash
docker-compose up --build
```

## 📡 API Endpoints

### Получить данные
```bash
GET /api/tickers/
```

### Параметры:

* symbol (BTCUSDT, ETHUSDT)
* start_time (timestamp)
* end_time (timestamp)

### Пример ответа:
```bash
[
  {
    "symbol": "BTCUSDT",
    "price": "50000.00",
    "timestamp": "2024-01-01T12:00:00Z"
  }
]
```