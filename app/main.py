from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
from controllers import dashboard, analytics, ports, docker, processes, startups, openvpn, header
from models.dashboard import DashboardData   
from models.analytics import AnalyticsData 

def update_system_data():
    DashboardData.get_data()
    AnalyticsData.get_data()
 

def create_app() -> FastAPI:
    app = FastAPI()

 
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_system_data, 'interval', seconds=300)
    scheduler.start()

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

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9393)
