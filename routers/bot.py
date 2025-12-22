from .. import models, schemas, utils, database, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from groq import Groq
from config import Config



router = APIRouter(
    tags=['ChatBot-test']
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Bot Coach Fitness</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get('/')
async def get():
    return HTMLResponse(html)



@router.websocket('/ws')
async def chatbot(websocket : WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
       
        api_key = str(Config.GROQ_KEY)
        try:
            client = Groq(api_key)

            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un chatbot que actua como un entrenador personal, dando consejos sobre fitness, responde solamente en texto plano, no uses nada mas, ningun comando para salto de linea ni simbolos, ni marcado de negrita. Si el usuario te habla en otro idioma como ingles, puedes responderle en ese idioma."},
                    {f"role": "user", "content": data}
                    ]
            )
            await websocket.send_text(resp.choices[0].message.content)
        except HTTPException as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")