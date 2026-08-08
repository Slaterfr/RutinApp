from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware


from models import models  # ADD THIS - Import models BEFORE create_engine()
from db.database import create_engine
from routers import routine, user, auth, bot, subRoutine, exercises, AIAnalyze, sessions, workoutsets, stadistics
from services.handlers import InvalidData


try:
    create_engine()
    print("database created")
except Exception as e:
    print(e)




app = FastAPI()
app.include_router(routine.router)
app.include_router(user.router)
app.include_router(bot.router)
app.include_router(auth.router)
app.include_router(subRoutine.router)
app.include_router(exercises.router)
app.include_router(sessions.router)
app.include_router(workoutsets.router)
app.include_router(AIAnalyze.router)
app.include_router(stadistics.router)

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app.add_middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=False,
        allow_headers=["*"]

)

# Custom handler for InvalidData exceptions (business logic errors)
@app.exception_handler(InvalidData)
async def invalid_data_handler(request: Request, exc: InvalidData):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": str(exc),
            "path": request.url.path
        },
    )

# Este decorador atrapa cualquier HTTPException que lances en tu código
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path
        },
    )

# Este atrapa errores inesperados (bugs reales) para que no crashee la conexión
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "critical_error",
            "message": "Algo salió muy mal en el servidor, estamos trabajando en ello.",
        },
    )









