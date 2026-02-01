from ..models import models
from ..db import database
from sqlmodel import SQLModel
import sqlmodel as sqml
from groq import Groq
from ..config import Config

api_key = Config.GROQ_KEY

def get_routine(id : int):
    with database.session as sess:
        rutina = sess.exec(sqml.select(models.Rutina).where(models.Rutina.id == id))
        return rutina

routine = get_routine(1)

prompt = """
Rutina: {routine}
"""
data = """Eres un chatbot que actua como un entrenador personal, dando consejos sobre fitness, responde solamente en texto plano, no uses nada mas, ningun comando para salto de linea ni simbolos, ni marcado de negrita. Si el usuario te habla en otro idioma como ingles, puedes responderle en ese idioma."""


client = Groq(api_key=api_key)

resp = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
            {"role": "system", "content": data},
            {f"role": "user", "content": prompt}
            ]
        )
print( resp.choices[0].message.content)








