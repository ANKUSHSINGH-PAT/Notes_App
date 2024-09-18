from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import logging
from models.note import note
from config.db import conn
from schemas.note import noteentity,notesentity

note=APIRouter()

templates = Jinja2Templates(directory="templates")

@note.get("/")
async def home():
    return {"message": "Hello, World!"}

@note.get("/items", response_class=HTMLResponse)
async def read_item(request: Request):
    logging.info("read_item")
    
    # Fetch documents from MongoDB
    docs = conn.MyDb.mytable.find({})
    mydocs = []
    
    for item in docs:
        print(item)  # Log the item
        mydocs.append({
            "id": str(item["_id"]),
            "title": str(item.get("title", "No Title")),  # Default value
            "desc": item.get("desc", "No Description"),    # Default value
            "important": item.get("important", False),     # Default value
        })

    return templates.TemplateResponse("index.html", {"request": request, "mydocs": mydocs})


@note.post("/items")
async def create_item(request: Request):
    form=await request.form()
    item_data={key:value for key, value in form.items()}
    conn.MyDb.mytable.insert_one(item_data)
    return{"message":"success"}
