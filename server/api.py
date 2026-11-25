import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from server.profiler import generate_profile_report
from server.cleaner import clean_dataset

app = FastAPI(
    title="Insyra API",
    description="Business Data Automation & Intelligence Engine",
    version="1.0.0"
)

# allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple test route
@app.get("/")
def home():
    return {"message": "Insyra API is running!"}

# Upload fike route (save to upload folder)
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    safe_name = os.path.basename(file.filename or "")
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename")
    file_path = os.path.join("uploads", safe_name)
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".csv",".xls", ".xlsx"]:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"message": "File uploaded!", "filename": safe_name}
    else:
        raise FastAPI.Exception(status_code=400, detail="Unsupported file format")

# Profile file route (returns profiler JSON)
@app.get("/profile/{filename}")

def get_profile(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    report = generate_profile_report(file_path)
    return reports

# Clean file route (cleans and saves to 'cleaned files')
@app.post("/clean/{filename}")
def clean_file(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    result = clean_dataset(file_path, output_dir="cleaned files")
    return {"message": "File cleaned!", "result": result}
