import asyncio
import aiohttp
import pandas as pd
from sklearn.metrics import f1_score
import joblib

TRAIN_SIZE = 5_000_000
port_api = "5000"

df = pd.read_csv("train.csv").drop("id", axis=1)
test_df = df[TRAIN_SIZE:]

pipeline = joblib.load('model-api/pipeline.joblib')
y_pred_model = pipeline.predict(test_df.drop("Response", axis=1))
y_true_model = test_df["Response"]

y_pred_api = []
y_true_api = []

async def send_request(session, url, data, y_true_api, y_pred_api, response_true):
    try:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                prediction = result["prediction"]
                y_pred_api.append(1 if prediction == "Response = 1" else 0)
                y_true_api.append(response_true)
    except Exception as e:
        print(f"Ошибка при запросе: {e}")

async def main():
    url = f"http://localhost:{port_api}/predict_model"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for row in test_df.itertuples(index=False, name="Row"):
            data = {
                "Gender": str(row.Gender),
                "Age": int(row.Age),
                "Driving_License": int(row.Driving_License),
                "Region_Code": float(row.Region_Code),
                "Previously_Insured": int(row.Previously_Insured),
                "Vehicle_Age": str(row.Vehicle_Age),
                "Vehicle_Damage": str(row.Vehicle_Damage),
                "Annual_Premium": float(row.Annual_Premium),
                "Policy_Sales_Channel": float(row.Policy_Sales_Channel),
                "Vintage": int(row.Vintage),
            }

            task = asyncio.create_task(send_request(session, url, data, y_true_api, y_pred_api, row.Response))
            tasks.append(task)

        await asyncio.gather(*tasks)

    print(f"f1 через модель: {f1_score(y_true_api, y_pred_api)}")
    print(f"f1 через api: {f1_score(y_true_model, y_pred_model)}")

if __name__ == "__main__":
    asyncio.run(main())