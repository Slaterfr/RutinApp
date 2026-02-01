from ..models import models
from ..db import database
from ..schemas import BotRequest
from ..dependencys import utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from groq import Groq
from ..config import Config
from ..services import AIService
import sqlmodel as sqlm
api_key = Config.GROQ_KEY

router = APIRouter(
    tags=['AI-Analysing'],
    prefix='/ai-analyze'
)

data = """Eres un chatbot que actua como un entrenador personal, dando consejos sobre fitness, responde solamente en texto plano, no uses nada mas, ningun comando para salto de linea ni simbolos, ni marcado de negrita. Si el usuario te habla en otro idioma como ingles, puedes responderle en ese idioma. En este caso, debes analizar los dias de la rutina del usuario, y decirme lo que ves y opinas."""

@router.get('/')
def analyze_rutine(id : int):
    with database.session as sess:
        rutina = sess.exec(sqlm.select(models.detalleEjercicio).join(models.DiaRutina).where(models.DiaRutina.routine_id==1)).fetchall()
        for day in rutina:
            print(day)
        prompt = str(rutina)

    client = Groq(api_key=api_key)

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
                {"role": "system", "content": data},
                {f"role": "user", "content": prompt}
                ]
            )
    print( resp.choices[0].message.content)
    
    return rutina