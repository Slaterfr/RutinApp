from models import models
from db import database
from schemas import BotRequest
from dependencys import utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter, WebSocket
from groq import Groq
from config import Config
import json
from datetime import datetime


router = APIRouter(
    prefix='/bot',
    tags=['ChatBot']
)


@router.websocket('/ws')
async def chatbot(websocket: WebSocket):
    """WebSocket endpoint for real-time AI fitness coach chat"""
    await websocket.accept()
    
    api_key = str(Config.GROQ_KEY)
    
    try:
        while True:
            # Receive message from frontend
            data = await websocket.receive_text()
            
            # Send acknowledgment that message was received
            await websocket.send_json({
                "type": "user_message",
                "content": data,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Get AI response from Groq
            try:
                client = Groq(api_key=api_key)
                
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un chatbot que actua como un entrenador personal, dando consejos sobre fitness, responde solamente en texto plano, no uses nada mas, ningun comando para salto de linea ni simbolos, ni marcado de negrita. Si el usuario te habla en otro idioma como ingles, puedes responderle en ese idioma."
                        },
                        {
                            "role": "user",
                            "content": data
                        }
                    ]
                )
                
                # Send bot response as JSON
                await websocket.send_json({
                    "type": "bot_message",
                    "content": resp.choices[0].message.content,
                    "timestamp": datetime.utcnow().isoformat(),
                    "model": "llama-3.3-70b-versatile"
                })
                
            except Exception as e:
                # Send error message as JSON
                await websocket.send_json({
                    "type": "error",
                    "content": f"Error processing response: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat()
                })
                
    except Exception as e:
        # Handle connection errors
        print(f"WebSocket connection error: {str(e)}")