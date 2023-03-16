from fastapi import FastAPI
from .routers import users, categorias, documentos

app = FastAPI()

app.include_router(users.router)
app.include_router(categorias.router)
app.include_router(documentos.router)