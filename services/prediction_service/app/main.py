from fastapi import FastAPI, HTTPException
from config import settings, logger
from models import ModelService
from schemas import PredictionRequest, PredictionResponse

app = FastAPI(
    title='Prediction Service',
    description='REST API exposing ML model predictions',
    version='0.1.0',
    )

model_service = ModelService(settings.models_dir)

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.post('/predict', response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        logger.info('Recived prediction request')
        prediction = model_service.predict(request.features)
        return PredictionResponse(result=prediction)
    except Exception as e:
        logger.error(f'Prediction error: {e}')
        raise HTTPException(status_code=500, detail='Prediction failed') 
