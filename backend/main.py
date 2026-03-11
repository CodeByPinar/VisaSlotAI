import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.database import Base, engine

# VeritabanÄ± tablolarÄ±nÄ± senkron olarak oluÅŸtur
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VisaSlotAI Dashboard Core API")

# CORS ayarlarÄ±: Frontend (3000) tarafÄ±ndan gelen isteklere ve tÃ¼m kÃ¶kenlere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Backend React derlenmiÅŸ (production) dosyalarÄ±na sunacak 
# Docker dÃ¼zeninde frontend klasÃ¶rÃ¼ "/app/frontend" yerine root klasÃ¶rde kaldÄ±ysa "frontend/build" olabilir
# Render Ã¼zerindeki build sÃ¼recimiz frontend'i compile edip etmedigini test etmek icin root adresinden staticFiles aÃ§arÄ±z
app.include_router(router)

# Production'da frontend folder mevcutsa Static olarak dÃ¶n 
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "build")

# EÄŸer ki proje derlenmiÅŸ frontend ile birlikte aÃ§Ä±lmaktaysa index.html ve diÄŸer assetleri serve et. 
if os.path.exists(FRONTEND_BUILD_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD_DIR, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "VisaSlotAI API is running. (Frontend is not built or path is missing. Use localhost:3000 in dev)"}
