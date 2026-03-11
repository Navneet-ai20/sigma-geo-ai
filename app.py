from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()

# Fix for CORS (Allows browser to talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE ---
USER_DB = {
    "admin": {"password": "sigma123", "secret": "engine"}
}

# --- MODELS ---
class LoginRequest(BaseModel):
    username: str
    password: str

class ResetRequest(BaseModel):
    username: str
    secret: str
    new_password: str

# --- ROUTES ---
@app.post("/login")
async def login(req: LoginRequest):
    if req.username in USER_DB and USER_DB[req.username]["password"] == req.password:
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.post("/reset")
async def reset(req: ResetRequest):
    if req.username in USER_DB and USER_DB[req.username]["secret"] == req.secret:
        USER_DB[req.username]["password"] = req.new_password
        return {"status": "success"}
    raise HTTPException(status_code=403, detail="Wrong Secret")

@app.post("/chat")
async def chat(data: dict):
    msg = data.get("text", "").lower()
    reply = f"Sigma AI analyzing: {msg}. Layer optimization active."
    if "pop" in msg: reply = "Analysis: High population density detected in urban clusters."
    return {"reply": reply}

@app.post("/report")
async def report(data: dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SIGMA ENGINEERING WORKS - REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Project Analysis:\n{data.get('content', 'No data')}")
    pdf.output("Sigma_Report.pdf")
    return FileResponse("Sigma_Report.pdf")

if __name__ == "__main__":
    # Use the PORT environment variable if available (for Render)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)