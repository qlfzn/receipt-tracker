# flowcessor

A web app that parses bank statement PDFs and returns structured cashflow data.

---

## Features

- Upload a bank statement PDF via drag-and-drop or file browser
- Extracts and structures transaction data using AI
- Displays summary stats (total transactions, credits, debits)
- Categorises transactions by payment channel (Direct / Payment Gateway)

## Tech Stack

**Backend**

- Python, FastAPI
- PyMuPDF — PDF text extraction
- Groq — AI-powered data structuring
- Pydantic

**Frontend**

- React, Vite
- Chakra UI
