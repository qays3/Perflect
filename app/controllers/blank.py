from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.templates import templates

from models.blank import BlankData

router = APIRouter()

@router.get("/blank", response_class=HTMLResponse)
async def blank(request: Request):
    data = BlankData()
    return templates.TemplateResponse(
        "blank.html",
        {"request": request, "title": "blank - Perflect Dashboard", "data": data}
    )
