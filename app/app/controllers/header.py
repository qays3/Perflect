from fastapi import APIRouter, HTTPException
<<<<<<< HEAD
from models.header import perform_reboot, get_resources_usage, get_resources_history
from fastapi.responses import JSONResponse
=======
from models.header import perform_reboot
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4

router = APIRouter()

@router.post("/reboot_system")
async def reboot():
    result = perform_reboot()
    if result['status'] == 'success':
        return result
    else:
<<<<<<< HEAD
        raise HTTPException(status_code=500, detail=result['message'])

@router.get("/api/resource-usage")
async def get_resource_usage():
    cpu_usage, ram_usage = get_resources_usage()
    return JSONResponse(content={"cpu_usage": cpu_usage, "ram_usage": ram_usage})

@router.get("/api/resource-history")
async def get_resource_history():
    cpu_history, ram_history = get_resources_history()
    return JSONResponse(content={"cpu_history": cpu_history, "ram_history": ram_history})
=======
        raise HTTPException(status_code=500, detail=result['message'])
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
