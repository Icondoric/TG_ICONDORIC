from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import cv, auth

app = FastAPI(title="Job Intermediation Platform NLP API", version="1.0.0")

# Configure CORS
origins = [
    "http://localhost:5173", # Vue default port
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.router, prefix="/api", tags=["cv"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Job Intermediation Platform API is running"}
