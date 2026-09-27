from fastapi import FastAPI
from .services import chat, pages

app = FastAPI()

app.include_router(chat.router, prefix="/ws")
app.include_router(pages.router)