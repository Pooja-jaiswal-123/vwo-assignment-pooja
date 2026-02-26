"""
main.py

Fixes & Enhancements Applied:
1. Fixed Uvicorn reload warning by passing application as an import string ("main:app").
2. Resolved naming collision between FastAPI endpoint and imported CrewAI task.
3. Added all 4 specialized agents and tasks to the Crew orchestration to complete the pipeline.
4. BONUS: Implemented SQLite database integration to store analysis results and user data.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import sqlite3
from datetime import datetime

from crewai import Crew, Process
# ✅ FIXED: Import ALL agents and tasks for the full pipeline
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import verification, analyze_financial_document, investment_analysis, risk_assessment

app = FastAPI(title="Financial Document Analyzer")

# ==========================================
# BONUS POINT: Database Setup
# ==========================================
def setup_db():
    """Initializes a local SQLite database to store analysis results."""
    conn = sqlite3.connect("analysis_results.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id TEXT PRIMARY KEY, filename TEXT, query TEXT, result TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# Run DB setup on startup
setup_db()


def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    # ✅ FIXED: Included all agents and tasks in logical sequence
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )
    
    # Passing file_path in inputs so tools can access the dynamically uploaded file
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

# ✅ FIXED: Renamed function to avoid shadowing the imported task
@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query:
            query = "Analyze this financial document for investment insights"
            
        # Process the document
        response = run_crew(query=query.strip(), file_path=file_path)
        final_output = str(response)
        
        # ==========================================
        # BONUS POINT: Save Results to Database
        # ==========================================
        conn = sqlite3.connect("analysis_results.db")
        c = conn.cursor()
        c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)", 
                  (file_id, file.filename, query, final_output, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "query": query,
            "analysis": final_output,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass 

if __name__ == "__main__":
    import uvicorn
    # ✅ FIXED: Uvicorn import string for reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)