import google.generativeai as genai
import json
import os
from typing import List, Dict, Any

# --- Gemini APIのセットアップ ---
# 環境変数からAPIキーを読み込む
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# --- Function Callingの定義 (校正機能で利用) ---
def summarize_text(summary: str):
    """Provided text's summary."""
    return {"summary": summary}

def propose_corrections(corrections: list[dict]):
    """Proposes corrections for a text."""
    return {"corrections": corrections}

tools = [summarize_text, propose_corrections]

# --- モデルの定義 ---
# 要約用のモデル
summarization_model = genai.GenerativeModel(model_name="gemini-2.5-flash")
# proofreading_model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", tools=tools) # 校正機能も後で実装予定

# --- ビジネスロジック ---

def execute_summarization(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って要約を実行する。
    """
    prompt = f"以下の文章を簡潔に要約してください。\n\n---\n{text}\n---"
    
    try:
        response = summarization_model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        # ここでAPIエラーのハンドリングを行う
        # 例: ロギング、デフォルトのメッセージを返すなど
        print(f"An error occurred: {e}")
        return {"summary": "要約の生成中にエラーが発生しました。"}

    return {"summary": summary}


def execute_proofreading(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って校正を実行する。
    """
    # ダミーの応答 (今回は変更なし)
    corrections = [
        {"original": "この文章は誤字があります。", "corrected": "この文章には誤字があります。", "reason": "助詞「は」が抜けていました。"},
        {"original": "不自然な表現だと思います", "corrected": "不自然な表現だと思われます。", "reason": "より丁寧な、断定を避ける表現に修正しました。"},
        {"original": "ユーザーに取って使いやすい。", "corrected": "ユーザーにとって使いやすい。", "reason": "誤字を修正しました。"}
    ]
    return {"corrections": corrections}
