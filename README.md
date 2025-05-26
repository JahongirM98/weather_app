# Weather Forecast App

Веб-приложение на Django для получения прогноза погоды по городу с использованием Open-Meteo API.

## 📌 Возможности

- Ввод города и отображение текущего прогноза (температура, ветер, время)
- Использование Open-Meteo API (поиск координат + текущая погода)
- Автоматическое сохранение последнего введённого города (через session)
- Сохранение истории введённых городов
- Подсказки при вводе с использованием `<datalist>`
- Очистка истории по кнопке
- Перенаправление после очистки, чтобы избежать повторного `?clear=1`
- API `/api/history` — выдаёт историю городов в JSON
- Динамическое автозаполнение из истории с помощью JavaScript
- Юнит-тесты: `GET`, `POST` с валидным и невалидным городом
- Docker-сборка и запуск через `docker-compose`

## 🛠 Используемые технологии

- Python 3.12
- Django 5.2
- requests
- HTML5, CSS
- Docker (опционально)

---

## 🚀 Как запустить без Docker

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
docker-compose up --build

