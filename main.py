from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
import os
import shutil
import uuid
import time
from qc_logic import evaluate_image

app = FastAPI()

# In-memory session store (for testing only)
active_sessions = {}

@app.get("/qc/session/{session_token}")
async def get_upload_form(session_token: str):
    if session_token not in active_sessions:
        raise HTTPException(status_code=404, detail="Invalid session token.")
    expires_at = active_sessions[session_token]
    if time.time() > expires_at:
        raise HTTPException(status_code=403, detail="Session expired.")
    html_content = f"""
    <html>
        <head><title>Upload Image for QC</title></head>
        <body>
            <h3>Upload Image for HDR QC</h3>
            <form action="/qc/session/{session_token}" method="post" enctype="multipart/form-data">
                <input name="file" type="file" accept="image/*">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/qc/session/{session_token}")
async def upload_file(session_token: str, file: UploadFile):
    if session_token not in active_sessions:
        raise HTTPException(status_code=404, detail="Invalid session token.")
    expires_at = active_sessions[session_token]
    if time.time() > expires_at:
        raise HTTPException(status_code=403, detail="Session expired.")
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    report = evaluate_image(temp_path)
    os.remove(temp_path)
    del active_sessions[session_token]  # One-time use
    return PlainTextResponse(report)
