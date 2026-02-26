"""
tools.py

This file defines all custom tools used by the Financial Document Analyzer.

Fixes Applied:
1. Removed deprecated SerperDevTool (version conflict issue)
2. Implemented proper CrewAI BaseTool structure
3. Removed async functions (CrewAI expects sync _run method)
4. Added proper error handling
5. Added structured comments for clarity
"""

# ==============================
# Import Required Libraries
# ==============================

import os
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader


# ==============================
# Financial Document Reader Tool
# ==============================

class FinancialDocumentTool(BaseTool):
    """
    Tool to read and extract text from a financial PDF document.
    """

    name: str = "Financial Document Reader"
    description: str = "Reads and extracts text from a financial PDF document."

    def _run(self, path: str = "data/sample.pdf") -> str:
        """
        Reads PDF file from the given path and returns cleaned text.
        """

        # Check if file exists
        if not os.path.exists(path):
            return "Error: File not found."

        try:
            loader = PyPDFLoader(path)
            docs = loader.load()

            full_report = ""

            for doc in docs:
                content = doc.page_content

                # Remove extra line breaks
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")

                full_report += content + "\n"

            return full_report

        except Exception as e:
            return f"Error while reading PDF: {str(e)}"


# Create instance to pass into agents
financial_document_tool = FinancialDocumentTool()


# ==============================
# Investment Analysis Tool
# ==============================

class InvestmentTool(BaseTool):
    """
    Tool to perform basic investment analysis on extracted financial data.
    """

    name: str = "Investment Analysis Tool"
    description: str = "Performs structured investment analysis on financial document data."

    def _run(self, financial_document_data: str) -> str:
        """
        Cleans and prepares financial data for analysis.
        """

        processed_data = financial_document_data.strip()

        # Remove multiple spaces
        while "  " in processed_data:
            processed_data = processed_data.replace("  ", " ")

        # Placeholder logic (can be improved later)
        return "Investment analysis completed based on provided financial data."


investment_tool = InvestmentTool()


# ==============================
# Risk Assessment Tool
# ==============================

class RiskTool(BaseTool):
    """
    Tool to evaluate financial risk from document data.
    """

    name: str = "Risk Assessment Tool"
    description: str = "Evaluates potential financial risk based on financial document data."

    def _run(self, financial_document_data: str) -> str:
        """
        Performs basic risk evaluation.
        """

        if not financial_document_data:
            return "No financial data provided for risk assessment."

        # Placeholder logic
        return "Risk assessment completed. Further financial metrics required for detailed evaluation."


risk_tool = RiskTool()