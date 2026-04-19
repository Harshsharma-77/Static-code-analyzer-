# CodeScan: Mini-C Static Code Analyzer

CodeScan is a comprehensive Compiler Design project demonstrating a full Static Analysis pipeline for a "Mini-C" language. Built with a Python backend and a responsive, modern HTML/JS frontend, this project performs Lexical, Syntax, and Semantic analysis.

## 🚀 Features

- **Lexical Analysis:** Regex-based tokenization of raw code strings.
- **Syntax Analysis:** Recursive descent parser that verifies grammar and catches missing semicolons or structural errors.
- **Semantic Analysis:** Symbol table generation to detect:
  - Undeclared variables
  - Type mismatches (e.g., assigning a `string` to an `int`)
  - Unused variables
- **Modern UI:** A beautiful, responsive frontend that communicates with the compiler API in real-time.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Compiler Components:** Custom-built Lexer, Parser, and Semantic Analyzer.

## 💻 How to Run Locally

1. Ensure you have Python installed.
2. Clone or download this repository.
3. Run the startup script:
   - **Windows:** Double-click `run.bat`
   - **Manual:** 
     ```bash
     pip install -r requirements.txt
     python main.py
     ```
4. Open your browser and navigate to `http://127.0.0.1:8000`.
