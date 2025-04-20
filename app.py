from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import os
from dotenv import load_dotenv
from email_pipeline import process_email_pipeline

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(title="Email Processing API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root_route():
    return {"message": "Welcome to compnent 3 of LeadXMail pipeling, Email generation and validation. Please route to /process-emails to process emails"}

@app.post("/process-emails")
async def process_emails(leads: List[Dict]):
    """
    Process email patterns for multiple leads.
    
    Args:
        leads: List of leads to process
    
    Returns:
        List of processed leads with email patterns
    """
    try:
        results = process_email_pipeline(leads)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

# Create ASGI application instance for Gunicorn
asgi_app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 