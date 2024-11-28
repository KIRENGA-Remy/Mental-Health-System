from fastapi import FastAPI
from .routers.user import router as user_router
from .routers.appointments import router as appointment_router
app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(appointment_router, prefix="/appointments", tags=["appointments"])
