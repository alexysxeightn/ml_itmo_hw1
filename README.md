### Запуск решения:
```
docker compose up -d 
```

На `localhost:5000` находится api:
- `/health` - проверка доступности
- `/stats` - получить количество запросов к api (в формате `{"request_count": 1}`)
- `/predict_model` - получить предсказание модели (принимает json с фичами, возвращает `{"prediction": "Response = 0/1"}`)

На `localhost:8501` находится веб-приложение:

![gif](https://drive.google.com/uc?export=view&id=1fCY6f46y_Fx4eSUJpwO0kuWyLGUQv9ef)

В качестве модели используется xgboost с предобработкой фичей (нормализация числовых и one hot категориальных). Обучение модели и анализ в `train.ipynb`

Тестирование api находится в `test_api.py`. После запуска скрипт обращается к api, делает предсказания и выводит F1 для полученных данных, а также F1 для инференса модели без api (метрики совпадают)

### Структура проекта:
```
└─ ml_itmo_hw1
   ├─ docker-compose.yaml
   ├─ model-api
   │  ├─ app_api.py
   │  ├─ Dockerfile
   │  ├─ pipeline.joblib
   │  └─ requirements.txt
   ├─ README.md
   ├─ streamlit-service
   │  ├─ Dockerfile
   │  ├─ requirements.txt
   │  └─ streamlit_app.py
   ├─ test_api.py
   └─ train.ipynb
```

### Команда:
- Хмелёв Алексей
- Васильев Тимур
- Шишкина Елена
