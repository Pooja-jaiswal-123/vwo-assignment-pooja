"""
agents.py

This file defines all AI agents used in the Financial Document Analyzer system.

Fixes Applied:
1. Updated CrewAI import (CrewAI v1.x compatible)
2. Proper LLM initialization
3. Fixed incorrect parameter name 'tool' → 'tools'
4. Removed deprecated search_tool import
5. Updated tool references to match refactored tools.py
6. Rewritten agents to provide realistic, compliant financial analysis by adding missing backstories.
"""

# ==============================
# Importing required libraries
# ==============================

import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM

# ✅ FIXED: Import correct tool instances
from tools import financial_document_tool, investment_tool, risk_tool

# ==============================
# LLM Configuration
# ==============================

llm = LLM(
    model="gpt-4o-mini",
    temperature=0.5
)

# ==============================
# Financial Analyst Agent
# ==============================

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze the provided financial document and generate accurate, data-driven financial insights based strictly on available information.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with expertise in financial statements, "
        "ratio analysis, and market trend evaluation. "
        "You provide evidence-based insights and avoid speculation."
    ),
    tools=[financial_document_tool],   # ✅ Correct tool instance
    llm=llm,
    allow_delegation=True
)

# ==============================
# Financial Document Verifier Agent
# ==============================

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether the uploaded document contains valid financial data and ensure the content is structured appropriately.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an elite Senior Auditor at a Big 4 accounting firm with 20 years of experience. "
        "Your expertise lies in catching discrepancies, verifying SEC filings, and ensuring "
        "financial reports are perfectly accurate before they reach stakeholders. You leave no stone unturned."
    ),
    tools=[financial_document_tool],   # optional but useful
    llm=llm,
    allow_delegation=True
)

# ==============================
# Investment Advisor Agent
# ==============================

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide responsible and risk-aware investment recommendations based on the financial analysis results.",
    verbose=True,
    backstory=(
        "You are a seasoned Wealth Manager and CFA charterholder. You specialize in asset allocation "
        "and portfolio management, always prioritizing your client's risk tolerance and long-term "
        "financial stability over short-term speculative gains."
    ),
    tools=[investment_tool],   # ✅ linked correctly
    llm=llm,
    allow_delegation=False
)

# ==============================
# Risk Assessment Agent
# ==============================

risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Evaluate financial risk based on financial metrics, volatility indicators, and business fundamentals.",
    verbose=True,
    backstory=(
        "You are a Chief Risk Officer (CRO) specializing in quantitative finance and enterprise risk management. "
        "You have a sharp eye for identifying liquidity crunches, market volatility exposures, and operational "
        "vulnerabilities in corporate balance sheets."
    ),
    tools=[risk_tool],   # ✅ linked correctly
    llm=llm,
    allow_delegation=False
)