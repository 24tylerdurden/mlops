from fastapi import FastAPI
import os, boto3, joblib
from src.train.train import S3_FILE_NAME, BUCKET_NAME
from pydantic import BaseModel

app = FastAPI()

model = None


def load_model():
    if not os.path.exists("model.pkl"):
        boto3.client("s3").download_file(BUCKET_NAME, S3_FILE_NAME, "model.pkl")
    return joblib.load("model.pkl")

class Input(BaseModel):
    features: list[float]


@app.post("/predict")
def predict(input: Input):
    pred = model.predict([input.features])[0]
    return {"prediction": int(pred)}


@app.on_event("startup")
def startup():
    global model
    model = load_model()

# if __name__ == "__main__":
#     uvicorn.run("app")