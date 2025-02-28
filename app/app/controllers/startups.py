<<<<<<< HEAD
from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from config.templates import templates
from models.startups import StartupsData

router = APIRouter()

@router.get("/startups", response_class=HTMLResponse)
async def syscontrols(request: Request):
    return templates.TemplateResponse(
        "startups.html",
        {"request": request, "title": "Startups - Perflect Dashboard"}
    )

@router.post("/syscontrols/add")
async def add_startup_file(file: UploadFile = File(...)):
    try:
        result = StartupsData.add_startup_file(file)
        return {"status": result}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
=======
from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from config.templates import templates
from models.startups import StartupsData

router = APIRouter()

@router.get("/startups", response_class=HTMLResponse)
async def syscontrols(request: Request):
    return templates.TemplateResponse(
        "startups.html",
        {"request": request, "title": "Startups - Perflect Dashboard"}
    )

@router.post("/syscontrols/add")
async def add_startup_file(file: UploadFile = File(...)):
    try:
        result = StartupsData.add_startup_file(file)
        return {"status": result}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
