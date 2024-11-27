from fastapi import APIRouter, HTTPException
from models.header import perform_reboot

router = APIRouter()

@router.post("/reboot_system")
async def reboot():
    result = perform_reboot()
    if result['status'] == 'success':
        return result
    else:
        raise HTTPException(status_code=500, detail=result['message'])