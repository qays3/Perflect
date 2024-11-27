from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.templates import templates
from models.ports import PortsData

router = APIRouter()

class PortActionRequest(BaseModel):
    port: int

@router.get("/ports", response_class=HTMLResponse)
async def ports(request: Request):
    data = PortsData.get_ports()
    return templates.TemplateResponse(
        "ports.html",
        {"request": request, "title": "Ports - Perflect Dashboard", "data": data},
    )

@router.post("/ports/open/{port}")
async def open_port(port: int):
    try:
        PortsData.open_port(port)
        data = PortsData.get_ports()
        return {"status": "Port opened", "port": port, "ports": data}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )

@router.post("/ports/close/{port}")
async def close_port(port: int):
    try:
        PortsData.close_port(port)
        data = PortsData.get_ports()
        return {"status": "Port closed", "port": port, "ports": data}
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )
