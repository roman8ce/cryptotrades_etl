# cryptocurrency_etl

Проект по сбору, обработке и визуализации данных криптовалютных торгов с использованием современного стека технологий.

## Обзор архитектуры

![pipline](https://github.com/user-attachments/assets/3f32bac6-86ed-4a6b-8609-da39cc1b12e9)

- Сбор данных с криптовалютных бирж через WebSocket
- Потоковая передача сообщений в реальном времени через Apache Kafka
- Хранение данных в PostgreSQL
- Трансформация данных с помощью Apache Airflow
- Визуализация данных в Apache Superset

## Используемые технологии

- **Apache Kafka**: Платформа потоковой передачи сообщений
- **PostgreSQL**: Хранение данных
- **Apache Airflow**: Оркестрация рабочих процессов
- **Apache Superset**: Визуализация данных
- **Python**: Основной язык программирования
- **Docker**: Контейнеризация

## Структура проекта

```
cryptocurrency_etl/
├── consumer/                # Реализация Kafka consumer
│   ├── Dockerfile
│   └── kafka_consumer.py
├── producer/               # Реализация Kafka producer
│   ├── Dockerfile
│   └── kafka_producer.py
├── dags/                   # Определения DAG для Airflow
│   └── ohlc.py
├── superset/              # Конфигурация графиков Superset
│   ├── Dockerfile
│   └── charts_creator.py
├── docker-compose.yml     # Конфигурация Docker сервисов
├── init.sql              # Скрипт инициализации базы данных
└── README.md
```

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/roman8ce/cryptotrades_etl
cd cryptocurrency_etl
```

2. Создайте файл `.env` с необходимыми переменными окружения:
```env
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
AIRFLOW__CORE__FERNET_KEY=your_fernet_key
AIRFLOW__WEBSERVER__SECRET_KEY=your_secret_key
```

3. Запустите сервисы:
```bash
docker-compose up -d --build
```

4. Доступ к сервисам:

| Сервис | URL | Логин/Пароль |
|--------|-----|--------------|
| Airflow | http://localhost:8080 | admin/admin |
| Superset | http://localhost:8088 | admin/admin |
| Kafka UI | http://localhost:8082 | - |

## Порты сервисов

| Сервис | Порт |
|--------|------|
| PostgreSQL | 5432 |
| Kafka | 9092 |
| Kafka UI | 8082 |
| Airflow | 8080 |
| Superset | 8088 |

## Доступные визуализации

1. График цены во времени (Линейный график)
2. График объема во времени (Столбчатая диаграмма)
3. OHLCV данные (Табличное представление)

## Разработка

Для модификации конвейера:

1. Настройте источники WebSocket в `producer/config.py`
2. Измените трансформации данных в `dags/ohlc.py`
3. Обновите настройки визуализации в `superset/charts_creator.py`
