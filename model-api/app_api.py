from fastapi import FastAPI, Request, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

pipeline = joblib.load('pipeline.joblib')

# Счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):
    Gender: str
    Age: int
    Driving_License: int
    Region_Code: float
    Previously_Insured: int
    Vehicle_Age: str
    Vehicle_Damage: str
    Annual_Premium: float
    Policy_Sales_Channel: float
    Vintage: int

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    # Создание DataFrame из данных
    new_data = pd.DataFrame({
        'Gender': [input_data.Gender],
        'Age': [input_data.Age],
        'Driving_License': [input_data.Driving_License],
        'Region_Code': [input_data.Region_Code],
        'Previously_Insured': [input_data.Previously_Insured],
        'Vehicle_Age': [input_data.Vehicle_Age],
        'Vehicle_Damage': [input_data.Vehicle_Damage],
        'Annual_Premium': [input_data.Annual_Premium],
        'Policy_Sales_Channel': [input_data.Policy_Sales_Channel],
        'Vintage': [input_data.Vintage],
    })

    # Предсказание
    predictions = pipeline.predict(new_data)

    # Преобразование результата в человеко-читаемый формат
    result = "Response = 1" if predictions[0] == 1 else "Response = 0"

    return {"prediction": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)