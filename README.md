# Financial Data Extraction, Preprocessing ,Visualization LLM Pipeline

This project extracts financial data from quarterly reports in PDF format, preprocesses the data, and provides visualization through a React-based dashboard. The solution is modular, with distinct components for data extraction, preprocessing, and visualization. A React dashboard and LLM chat front is included for enhanced user interaction and analysis.

project_quater_analysis\
├── data_scrapping\
│   ├── conf.yaml
│   ├── data\
│   │   └── raw\
│   │       ├── DIPD\
│   │       └── REXP\
│   ├── outputs\
│   ├── prompts\
│   │   ├── extraction_prompt.jinja2
│   │   └── preprocessing_prompt.jinja2
│   └── src\
│       ├── agents\
│       │   └── agents.py
│       ├── extraction\
│       │   └── extraction.py
│       ├── pipeline\
│       │   └── main.py       <-- Main pipeline: downloads PDFs, extracts and preprocesses data
│       ├── preprocessing\
│       │   └── preprocessing.py
│       ├── scrapper\
│       │   └── download_pdf.py
│       └── utils\
│           ├── config_utils.py
│           └── template_utils.py

├── financial-dashboard\
│   ├── backend\
│   │   ├── main.py                         <-- Backend for dashboard and LLM
│   │   └── models\
│   │       ├── dashboard_data_agent.py
│   │       └── llm_query.py
│   ├── public\
│   └── src\
│       ├── App.jsx
│       ├── ChatIcon.jsx
│       ├── chat\
│       │   ├── chat.css
│       │   └── FinancialChat.jsx
│       └── components\
│           └── dashboard\
│               ├── Dashboard.jsx
│               ├── FilterBar.jsx
│               ├── StatsCards.jsx
│               └── charts\
│                   ├── GrossProfitChart.jsx
│                   ├── NetIncomeChart.jsx
│                   └── RevenueChart.jsx



## ⚙️ 2. Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **npm**

---

## 🚀 3. Setup Instructions

### A. Clone the Repository

```bash
git clone https://github.com/amayaambagaspitiya/financial_dashboard.git
cd financial_dashboard
```

### B. Create and Activate a Virtual Environment and Run Data scrapping


cd data_scrapping
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.pipeline.main     


## B. Running the React Dashboard

1. **Navigate to the Dashboard Folder:**
   
   docker compose up --build (run this only if running for new data)
   docker compose up  (run this only if you are running the static data file )

   ```


2. **View Dashboard and Chat:**
   - Access via [http://localhost:3000](http://localhost:3000) (for dashboard)
   - http://localhost:3000/chatbot (For chatbot)

---

## 6. Project Details

### 6.1. Data Extraction and Preprocessing
- Download pdfs : download pdfs when the website link is privided using selenium    
- Extraction: Financial figures are extracted from quarterly PDF reports using OpenAI-based prompts.
- Preprocessing:Extracted data is cleaned, normalized using OpenAI-based prompts, and enriched with metadata like quarter and year. The processed data is saved in CSV and JSON formats. one processed_data.json file saves inside  the financial-dashboard/backend/data folder so that json file can use for dashboard and llm

### 6.2. Visualization

- The React dashboard visualizes financial data, enabling users to explore metrics interactively.
- A chat feature is integrated for querying financial data


