from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config.templates import templates
from models.processes import ProcessManagement, ProcessesData

router = APIRouter()

@router.get("/processes", response_class=HTMLResponse)
async def processes(request: Request):
    processes_data = ProcessManagement.get_processes()
    return templates.TemplateResponse(
        "processes.html",
        {"request": request, "processes": processes_data.processes}
    )

@router.post("/kill/{pid}", response_class=HTMLResponse)
async def kill_process(request: Request, pid: int):
    result = ProcessManagement.kill_process(pid)

    processes_data = ProcessManagement.get_processes()
    return templates.TemplateResponse(
        "processes.html",
        {
            "request": request,
            "processes": processes_data.processes,
            "message": result
        }
    )

@router.post("/kill_force/{pid}", response_class=HTMLResponse)
async def kill_process_force(request: Request, pid: int):
    result = ProcessManagement.kill_process_force(pid)
    processes_data = ProcessManagement.get_processes()
    return templates.TemplateResponse(
        "processes.html",
        {
            "request": request,
            "processes": processes_data.processes,
            "message": result
        }
    )
