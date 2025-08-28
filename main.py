from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

# コアロジックをインポート
from core import execute_summarization, execute_proofreading

app = FastAPI(
    title="AI Writing Assistant API",
    description="An API to summarize and proofread texts using Gemini.",
    version="1.0.0",
)

# --- CORSミドルウェアの設定 ---
# フロントエンドのReactアプリ（ポート3000）からのアクセスを許可する
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- APIのデータモデル定義 (Pydantic) ---

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="処理対象のテキスト")

class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="要約されたテキスト")

class CorrectionItem(BaseModel):
    original: str
    corrected: str
    reason: str

class ProofreadResponse(BaseModel):
    corrections: List[CorrectionItem] = Field(..., description="修正提案のリスト")


# --- APIエンドポイント定義 ---

@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(payload: TextInput):
    """
    受け取ったテキストを要約します。
    """
    result = execute_summarization(payload.text)
    return result

@app.post("/proofread", response_model=ProofreadResponse)
def proofread_endpoint(payload: TextInput):
    """
    受け取ったテキストを校正し、修正案を返します。
    """
    result = execute_proofreading(payload.text)
    return result

@app.get("/", include_in_schema=False)
def root():
    return {"message": "AI Writing Assistant API is running."}
