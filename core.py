import google.generativeai as genai
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# --- Gemini APIのセットアップ ---
# 環境変数からAPIキーを読み込む
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# --- モデルの定義 ---
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# --- ビジネスロジック ---

def execute_summarization(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って要約を実行する。
    """
    prompt = f"""以下の文章を簡潔に要約してください。

---
{text}
---"""
    
    try:
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return {"summary": "要約の生成中にエラーが発生しました。"}

    return {"summary": summary}


def execute_proofreading(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って校正を実行する。
    """
    prompt = f"""あなたはプロの編集者です。以下の文章を校正し、修正点を指摘してください。
修正点が見つかった場合は、以下のJSON形式のリストで回答してください。修正がない場合は空のリスト `[]` を返してください。

形式:
[
  {{
    "original": "修正前の単語やフレーズ",
    "corrected": "修正後の単語やフレーズ",
    "reason": "修正理由を簡潔に説明"
  }}
]

文章:
---
{text}
---
"""
    
    try:
        # API呼び出し時にJSONモードを指定
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        corrections = json.loads(response.text)
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API response: {e}")
        # フロントエンドが空のリストを期待している可能性を考慮
        return {"corrections": []}
    except Exception as e:
        print(f"An error occurred during proofreading: {e}")
        return {"corrections": []}

    return {"corrections": corrections}

