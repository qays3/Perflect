from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.templates import templates
from models.dashboard import DashboardData

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    data = DashboardData.get_data()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "title": "Home - Perflect Dashboard", "data": data}
    )

@router.get("/api/system-data")
async def get_system_data():
    current_data = DashboardData.get_data()
    historical_data = DashboardData.get_historical_data()
    return {"current_data": current_data.dict(), "historical_data": historical_data}


