import google.generativeai as genai
import json
from typing import List, Dict, Any

# --- Gemini APIのセットアップ ---
# genai.configure(api_key="YOUR_GEMINI_API_KEY")

# --- Function Callingの定義 ---
def summarize_text(summary: str):
    """Provided text's summary."""
    return {"summary": summary}

def propose_corrections(corrections: list[dict]):
    """Proposes corrections for a text."""
    return {"corrections": corrections}

tools = [summarize_text, propose_corrections]
# model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", tools=tools)

# --- ビジネスロジック ---

def execute_summarization(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って要約を実行する。
    """
    # ダミーの応答
    return {"summary": f"「{text[:40]}...」の要約結果です。簡潔で分かりやすい文章は、読み手の理解を助けます。"}


def execute_proofreading(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って校正を実行する。
    """
    # ダミーの応答
    corrections = [
        {"original": "この文章は誤字があります。", "corrected": "この文章には誤字があります。", "reason": "助詞「は」が抜けていました。"},
        {"original": "不自然な表現だと思います", "corrected": "不自然な表現だと思われます。", "reason": "より丁寧な、断定を避ける表現に修正しました。"},
        {"original": "ユーザーに取って使いやすい。", "corrected": "ユーザーにとって使いやすい。", "reason": "誤字を修正しました。"}
    ]
    return {"corrections": corrections}
