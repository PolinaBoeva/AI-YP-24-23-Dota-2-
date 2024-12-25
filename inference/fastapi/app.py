import uvicorn
from fastapi import FastAPI
from api.v1.models import routes as models_routes

app = FastAPI(
    title="Predictive Models Dota2 API",
    version="1.0",
    description="API для обучения моделей предсказания исхода игр (Radiant/Dire)."
)

app.include_router(models_routes.router, prefix="/api/v1/models", tags=["models"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
