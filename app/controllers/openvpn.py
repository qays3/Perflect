# /home/hidden/Downloads/DashBoard/app/controllers/openvpn.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from models.openvpn import OpenVPNData
from config.templates import templates


router = APIRouter()

@router.get("/openvpn", response_class=HTMLResponse)
async def openvpn(request: Request):
    data = OpenVPNData()

    return templates.TemplateResponse(
        "openvpn.html", 
        {"request": request, "title": "OpenVPN - Perflect Dashboard", "data": data}
    )

@router.post("/generate_openvpn", response_class=FileResponse)
async def generate_openvpn(request: Request):
    data = OpenVPNData(client_name="client")

    generated_file = data.generate_ovpn_file()
    
    if generated_file:
        return FileResponse(generated_file, media_type="application/octet-stream", filename="client.ovpn")
    return {"message": "Error generating OpenVPN file"}
