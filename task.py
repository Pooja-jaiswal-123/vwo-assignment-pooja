"""
task.py

Fixes Applied:
1. Fixed incorrect imports (removed deprecated search_tool).
2. Assigned specific agents to their respective tasks instead of overloading one agent.
3. Fixed tool referencing (used instantiated tools from tools.py).
4. Completely rewrote prompt descriptions and expected_outputs to strictly prevent hallucinations, enforce data accuracy, and provide compliant financial advice.
"""

from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import financial_document_tool, investment_tool, risk_tool

# ==========================================
# Task 1: Document Verification
# ==========================================
verification = Task(
    description=(
        "Carefully read and verify the uploaded document for the user's query: {query}. "
        "Confirm whether it is a valid financial document (e.g., balance sheet, income statement, 10-K). "
        "Extract key metadata such as company name, reporting period, and document type. "
        "Strictly rely on the provided text. Do NOT hallucinate or make assumptions."
    ),
    expected_output=(
        "A brief verification report stating the document's validity, type, and key metadata. "
        "If it is not a financial document, explicitly state so and halt further analysis."
    ),
    agent=verifier,
    tools=[financial_document_tool],
    async_execution=False
)

# ==========================================
# Task 2: Financial Analysis
# ==========================================
analyze_financial_document = Task(
    description=(
        "Based on the verified document, analyze the core financial metrics relevant to the query: {query}. "
        "Extract actual numbers regarding revenue, expenses, margins, or other relevant KPIs. "
        "Do NOT make up any numbers, trends, or URLs. Only state facts found in the text."
    ),
    expected_output=(
        "A structured financial summary using bullet points with actual data points extracted "
        "from the document, including key ratios or metrics if available in the text."
    ),
    agent=financial_analyst,
    tools=[financial_document_tool],
    async_execution=False
)

# ==========================================
# Task 3: Investment Analysis
# ==========================================
investment_analysis = Task(
    description=(
        "Using the accurate financial analysis provided by the analyst, formulate sensible, "
        "data-backed investment insights relevant to the query: {query}. "
        "Avoid speculative or dangerous recommendations. Base all advice strictly on the verified financial health of the entity."
    ),
    expected_output=(
        "A conservative, professional investment advisory report detailing potential opportunities "
        "and why they align with the extracted financial data. Do not include fake URLs."
    ),
    agent=investment_advisor,
    tools=[investment_tool], 
    async_execution=False
)

# ==========================================
# Task 4: Risk Assessment
# ==========================================
risk_assessment = Task(
    description=(
        "Evaluate the financial data and analysis for potential risks relevant to the query: {query}. "
        "Identify factual liquidity, market, or operational risks explicitly present or strongly implied by the actual numbers. "
        "Do NOT invent catastrophic scenarios or use fake hedging strategies."
    ),
    expected_output=(
        "A professional risk assessment report highlighting key vulnerabilities backed by specific "
        "data points from the financial document. Avoid contradictory guidelines."
    ),
    agent=risk_assessor,
    tools=[risk_tool],
    async_execution=False
)