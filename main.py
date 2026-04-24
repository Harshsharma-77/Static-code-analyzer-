from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

from analyzer.lexer import Lexer
from analyzer.parser import Parser
from analyzer.semantic import SemanticAnalyzer

app = FastAPI(title="CodeScan Mini-C Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    code: str
    language: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/analyze")
async def analyze_code(req: AnalyzeRequest):
    code = req.code
    
    # Initialize pipeline
    lexer = Lexer()
    parser = Parser()
    semantic = SemanticAnalyzer()
    
    all_issues = []
    
    # 1. Lexical Analysis
    tokens, lex_issues = lexer.tokenize(code)
    all_issues.extend(lex_issues)
    
    # 2. Syntax Analysis
    ast, parse_issues = parser.parse(tokens)
    all_issues.extend(parse_issues)
    
    # 3. Semantic Analysis
    sem_issues = semantic.analyze(ast)
    all_issues.extend(sem_issues)
    
    # Calculate score based on issues
    score = 100
    for issue in all_issues:
        if issue["severity"] == "error":
            score -= 20
        elif issue["severity"] == "warning":
            score -= 5
        else:
            score -= 2
            
    score = max(0, score)
    
    return {
        "language": "Mini-C",
        "score": score,
        "issues": all_issues
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

