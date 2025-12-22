from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from . import models, database, schemas
from .routers import routine, user, auth, bot,subRoutine


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












