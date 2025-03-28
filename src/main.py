from typing import Union
from fastapi import FastAPI 
from api.data import router as data_router
from api.strategy import router as strategy_router

app = FastAPI() 
app.include_router(data_router, prefix='/api/data')
app.include_router(strategy_router, prefix='/api/strategy')
