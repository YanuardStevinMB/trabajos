from __future__ import annotations
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.analyzer import SUPPORTED_CROPS, analyze_image
from app.database import get_analysis, init_db, list_analyses, save_analysis, stats

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
MAX_IMAGE_BYTES=8*1024*1024
ALLOWED_TYPES={"image/jpeg","image/png","image/webp"}

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app=FastAPI(
    title="AgroVision API",version="1.0.0",
    description="Prototipo funcional para detección temprana de posibles afectaciones visuales en cultivos.",
    lifespan=lifespan
)
app.mount("/static",StaticFiles(directory=STATIC_DIR),name="static")

@app.get("/",include_in_schema=False)
def home()->FileResponse: return FileResponse(STATIC_DIR/"index.html")

@app.get("/health")
def health()->dict: return {"status":"ok","service":"agrovision"}

@app.get("/api/crops")
def crops()->list[dict]: return [{"code":c,"name":n} for c,n in SUPPORTED_CROPS.items()]

@app.get("/api/stats")
def analysis_stats()->dict: return stats()

@app.get("/api/analyses")
def analyses(limit:int=20)->list[dict]:
    return list_analyses(max(1,min(limit,100)))

@app.get("/api/analyses/{analysis_id}")
def analysis_detail(analysis_id:int)->dict:
    data=get_analysis(analysis_id)
    if not data: raise HTTPException(status_code=404,detail="Análisis no encontrado")
    return data

@app.post("/api/analyses",status_code=201)
async def create_analysis(crop:str=Form(...), image:UploadFile=File(...))->dict:
    if crop not in SUPPORTED_CROPS: raise HTTPException(status_code=422,detail="Cultivo no soportado")
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415,detail="Formato no permitido. Use JPG, PNG o WEBP")
    raw=await image.read(MAX_IMAGE_BYTES+1)
    if len(raw)>MAX_IMAGE_BYTES: raise HTTPException(status_code=413,detail="La imagen supera el tamaño máximo de 8 MB")
    try: result=analyze_image(raw,crop)
    except ValueError as exc: raise HTTPException(status_code=422,detail=str(exc)) from exc
    analysis_id=save_analysis(crop,image.filename or "imagen",result)
    saved=get_analysis(analysis_id); assert saved is not None
    return saved
