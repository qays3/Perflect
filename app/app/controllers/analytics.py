<<<<<<< HEAD
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.templates import templates
from models.analytics import AnalyticsData

router = APIRouter()

@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    return templates.TemplateResponse(
        "analytics.html", {"request": request, "title": "Analytics - Perflect Dashboard"}
    )

@router.get("/api/analytics-data")
async def get_analytics_data():
    current_data = AnalyticsData.get_data()
    historical_data = AnalyticsData.get_historical_data()

    return {
        "current_data": current_data.dict(),
        "historical_data": historical_data
    }
=======
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.templates import templates
from models.analytics import AnalyticsData

router = APIRouter()

@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    return templates.TemplateResponse(
        "analytics.html", {"request": request, "title": "Analytics - Perflect Dashboard"}
    )

@router.get("/api/analytics-data")
async def get_analytics_data():
    current_data = AnalyticsData.get_data()
    historical_data = AnalyticsData.get_historical_data()

    return {
        "current_data": current_data.dict(),
        "historical_data": historical_data
    }
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
