from fastapi import FastAPI
from project.routers.user import router as user_router
from project.routers.appointments import router as appointment_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(appointment_router, prefix="/appointments", tags=["appointments"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("project.main:app", host="127.0.0.1", port=8000, reload=True)
