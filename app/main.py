from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config.templates import templates
from controllers import dashboard, analytics, ports, docker, processes, startups, openvpn, header

from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
from models.dashboard import DashboardData
from models.analytics import AnalyticsData   

async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_system_data, 'interval', minutes=30)
    scheduler.start()
    yield

def update_system_data():
    DashboardData.get_data()   
    AnalyticsData.get_data()  

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/json", StaticFiles(directory="json"), name="json")

app.include_router(dashboard.router)
app.include_router(analytics.router)   
app.include_router(ports.router)
app.include_router(docker.router)
app.include_router(processes.router)
app.include_router(startups.router)
app.include_router(openvpn.router)
app.include_router(header.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9393)
