from fastapi import FastAPI, Body, Response, status, HTTPException, Depends

from .db import database
from .routers import routine, user, auth, bot,subRoutine, exercises


try:
    database.create_engine()
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











