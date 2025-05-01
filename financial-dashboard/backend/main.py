from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.llm_query import answer_query
from models.dashboard_data_agent import DashboardDataAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

dashboard_agent = DashboardDataAgent()

@app.post("/query")
def query_financial_data(request: QueryRequest):
    print("Received query:", request.query)
    if not request.query.strip():
        return {"answer": "Please enter a valid question."}
    try:
        df = dashboard_agent.get_raw_df()
        answer = answer_query(request.query, df)
        return {"answer": answer}
    except Exception as e:
        print("Error during query processing:", e)
        return {"answer": f"Error: {str(e)}"}

@app.get("/dashboard-data")
def get_dashboard_data():
    try:
        return dashboard_agent.get_full_data()
    except Exception as e:
        return {"error": str(e)}
