import os
import shutil
from fastapi import FastAPI, UploadFile, File
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
    file_path = f"uploads/{file.filename}"
    # save file to disk
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "File uploaded!", "filename": file.filename}

# Profile file route (returns profiler JSON)
@app.get("/profile/{filename}")
def get_profile(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    report = generate_profile_report(file_path)
    return report

# Clean file route (cleans and saves to 'cleaned files')
@app.post("/clean/{filename}")
def clean_file(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    result = clean_dataset(file_path, output_dir="cleaned files")
    return {"message": "File cleaned!", "result": result}
