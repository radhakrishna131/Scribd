from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
app=FastAPI(title='StudyScript API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173'],allow_methods=['*'],allow_headers=['*'])
app.include_router(router)
app.mount('/generated',StaticFiles(directory=Path(__file__).resolve().parents[1]/'generated'),name='generated')
