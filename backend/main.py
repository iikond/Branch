from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .services import chat

BASE_DIR = Path(__file__).resolve().parent

# Папка frontend — это корень для всей статики и страниц
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI()

app.include_router(chat.router, prefix="/ws")

# Монтируем всю папку frontend в /static
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "static"),
    name="static"
)

@app.get("/")
@app.get("/board")
async def board():
    html_path = FRONTEND_DIR / "pages" / "board.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@app.get("/chats")
async def board():
    html_path = FRONTEND_DIR / "pages" / "chats.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@app.get("/events")
async def board():
    html_path = FRONTEND_DIR / "pages" / "events.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@app.get("/notes")
async def board():
    html_path = FRONTEND_DIR / "pages" / "notes.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@app.get("/tasks")
async def board():
    html_path = FRONTEND_DIR / "pages" / "tasks.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)