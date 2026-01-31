import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import cv, auth
from app.api.routes import ml_predictions, institutional_profiles
from app.services.ml_integration_service import get_ml_service

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos de ciclo de vida de la aplicacion
    """
    # Startup: Cargar modelo ML
    logger.info("Iniciando aplicacion...")
    try:
        ml_service = get_ml_service()
        if ml_service.is_ready:
            logger.info("Modelo ML cargado correctamente")
        else:
            logger.warning("Modelo ML no disponible al inicio")
    except Exception as e:
        logger.error(f"Error cargando modelo ML: {e}")

    yield

    # Shutdown
    logger.info("Cerrando aplicacion...")


app = FastAPI(
    title="Job Intermediation Platform API",
    description="API para intermediacion laboral con ML",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Vue default port
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers existentes
app.include_router(cv.router, prefix="/api", tags=["CV Processing"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Nuevos routers Fase 6
app.include_router(
    ml_predictions.router,
    prefix="/api/ml",
    tags=["Machine Learning"]
)
app.include_router(
    institutional_profiles.router,
    prefix="/api/admin",
    tags=["Admin - Institutional Profiles"]
)


@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint"""
    return {
        "message": "Job Intermediation Platform API is running",
        "version": "2.0.0",
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check"""
    ml_service = get_ml_service()
    return {
        "status": "healthy",
        "ml_model_loaded": ml_service.is_ready,
        "version": "2.0.0"
    }
