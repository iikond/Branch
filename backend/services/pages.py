from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"

# Монтируем статику (CSS, JS, картинки)
router.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "static"),
    name="static"
)

# Инициализируем шаблонизатор, указывая корень frontend
# (чтобы из любого места были доступны и pages/, и components/)
templates = Jinja2Templates(directory=FRONTEND_DIR)


@router.get("/")
@router.get("/board")
async def board(request: Request):
    html_path = FRONTEND_DIR / "pages" / "board.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")

    # Передаём request отдельно, а словарь — через context
    return templates.TemplateResponse(
        request=request, 
        name="pages/board.html", 
        context={}
    )

@router.get("/chats")
async def chats(request: Request):
    html_path = FRONTEND_DIR / "pages" / "chats.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request=request, 
        name="pages/chats.html", 
        context={}
    )

@router.get("/events")
async def events(request: Request):
    html_path = FRONTEND_DIR / "pages" / "events.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request=request, 
        name="pages/events.html", 
        context={}
    )

@router.get("/notes")
async def notes(request: Request):
    html_path = FRONTEND_DIR / "pages" / "notes.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request=request, 
        name="pages/notes.html", 
        context={}
    )

@router.get("/tasks")
async def tasks(request: Request):
    html_path = FRONTEND_DIR / "pages" / "tasks.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request=request, 
        name="pages/tasks.html", 
        context={}
    )

@router.get("/reg")
async def reg(request: Request):
    html_path = FRONTEND_DIR / "pages" / "reg.html"
    if not html_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        request=request, 
        name="pages/reg.html", 
        context={}
    )