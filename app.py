from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from pymongo import MongoClient

# MongoDB connection setup
try:
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn["MyDb"]
    collections = db["mytable"]
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")

# Logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home():
    return {"message": "Hello, World!"}

@app.get("/items", response_class=HTMLResponse)
async def read_item(request: Request):
    logging.info("read_item")
    
    # Fetch documents from MongoDB
    docs = collections.find({})
    mydocs = []
    for doc in docs:
        print(doc)
        mydocs.append({
            "id": str(doc["_id"]),
            "note": doc.get("note", "")  
        })

    # Render the template with the documents
    return templates.TemplateResponse("index.html", {"request": request, "mydocs": mydocs})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
