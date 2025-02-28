<<<<<<< HEAD
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse  
from models.docker import DockerOperations
from config.templates import templates

router = APIRouter()

@router.get("/docker", response_class=HTMLResponse)
async def docker(request: Request):
    containers = DockerOperations.get_running_containers()
    return templates.TemplateResponse("docker.html", {"request": request, "title": "Docker - Perflect Dashboard", "containers": containers})

@router.get("/docker/containers")
async def get_running_containers():
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"containers": [container.dict() for container in containers]})

@router.post("/docker/stop/{container_id}")
async def stop_docker_container(container_id: str):
    result_message = DockerOperations.stop_container(container_id)
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})

@router.post("/docker/clean_cache")
async def clean_docker_cache():
    result_message = DockerOperations.clean_cache()
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})

@router.post("/docker/stop_all")
async def stop_all_docker_containers():
    result_message = DockerOperations.stop_all_containers()
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})


@router.post("/docker/run")
async def run_docker_container(request: Request):
    try:
        body = await request.json()
        image = body.get("image")

        if not image:
            return JSONResponse(status_code=422, content={"error": "Image is required"})

        command = f"{image}"
        result_message = DockerOperations.run_container_with_command(command)

        containers = DockerOperations.get_running_containers()
        return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})
    except Exception as e:
=======
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse  
from models.docker import DockerOperations
from config.templates import templates

router = APIRouter()

@router.get("/docker", response_class=HTMLResponse)
async def docker(request: Request):
    containers = DockerOperations.get_running_containers()
    return templates.TemplateResponse("docker.html", {"request": request, "title": "Docker - Perflect Dashboard", "containers": containers})

@router.get("/docker/containers")
async def get_running_containers():
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"containers": [container.dict() for container in containers]})

@router.post("/docker/stop/{container_id}")
async def stop_docker_container(container_id: str):
    result_message = DockerOperations.stop_container(container_id)
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})

@router.post("/docker/clean_cache")
async def clean_docker_cache():
    result_message = DockerOperations.clean_cache()
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})

@router.post("/docker/stop_all")
async def stop_all_docker_containers():
    result_message = DockerOperations.stop_all_containers()
    containers = DockerOperations.get_running_containers()
    return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})


@router.post("/docker/run")
async def run_docker_container(request: Request):
    try:
        body = await request.json()
        image = body.get("image")

        if not image:
            return JSONResponse(status_code=422, content={"error": "Image is required"})

        command = f"{image}"
        result_message = DockerOperations.run_container_with_command(command)

        containers = DockerOperations.get_running_containers()
        return JSONResponse(content={"message": result_message, "containers": [container.dict() for container in containers]})
    except Exception as e:
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
        return JSONResponse(status_code=500, content={"error": f"Unexpected error: {str(e)}"})