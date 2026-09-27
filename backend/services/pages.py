from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent

# Папка frontend — это корень для всей статики и страниц
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"

# Монтируем всю папку frontend в /static
router.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "static"),
    name="static"
)

@router.get("/")
@router.get("/board")
async def board():
    html_path = FRONTEND_DIR / "pages" / "board.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@router.get("/chats")
async def board():
    html_path = FRONTEND_DIR / "pages" / "chats.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@router.get("/events")
async def board():
    html_path = FRONTEND_DIR / "pages" / "events.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@router.get("/notes")
async def board():
    html_path = FRONTEND_DIR / "pages" / "notes.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)

@router.get("/tasks")
async def board():
    html_path = FRONTEND_DIR / "pages" / "tasks.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(html_path)