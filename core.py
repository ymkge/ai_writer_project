import google.generativeai as genai
import json
import os
import re
import csv
from typing import Dict, Any, List
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# --- 設定の読み込み ---
try:
    with open("prompt_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    raise RuntimeError("Configuration file 'prompt_config.json' not found.")
except json.JSONDecodeError:
    raise RuntimeError("Could not decode 'prompt_config.json'. Please check for syntax errors.")


# --- Gemini APIのセットアップ ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# --- 結果保存ディレクトリの設定 ---
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- CSV保存関数 ---
def save_summary_to_csv(original_text: str, summary: str):
    file_path = os.path.join(RESULTS_DIR, "summaries.csv")
    fieldnames = ["Original Text", "Summary"]
    
    file_exists = os.path.exists(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader() # Write header only if file is new
            
        writer.writerow({"Original Text": original_text, "Summary": summary})
    print(f"Summary saved to {file_path}")

def save_proofreading_to_csv(original_text: str, corrections: List[Dict[str, str]]):
    file_path = os.path.join(RESULTS_DIR, "proofreadings.csv")
    fieldnames = ["Original Text", "Original Phrase", "Corrected Phrase", "Reason"]
    
    file_exists = os.path.exists(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader() # Write header only if file is new
            
        # Write each correction as a separate row, linking to the original text
        for correction in corrections:
            row = {
                "Original Text": original_text,
                "Original Phrase": correction.get("original", ""),
                "Corrected Phrase": correction.get("corrected", ""),
                "Reason": correction.get("reason", "")
            }
            writer.writerow(row)
    print(f"Proofreading results saved to {file_path}")


# --- ビジネスロジック ---

def execute_summarization(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って要約を実行する。
    設定は prompt_config.json から読み込む。
    """
    try:
        conf = config['summarize']
        model = genai.GenerativeModel(model_name=conf['model'])
        prompt = conf['prompt_template'].format(text=text)
        
        response = model.generate_content(
            prompt,
            generation_config=conf['generation_config']
        )
        summary = response.text
    except KeyError as e:
        print(f"Configuration error: Missing key {e} in 'summarize' config.")
        return {"summary": "設定ファイルエラーが発生しました。"}
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return {"summary": "要約の生成中にエラーが発生しました。"}

    return {"summary": summary}


def execute_proofreading(text: str) -> Dict[str, Any]:
    """
    テキストを受け取り、Gemini APIを使って校正を実行する。
    設定は prompt_config.json から読み込む。
    """
    json_str = ""
    try:
        conf = config['proofread']
        model = genai.GenerativeModel(model_name=conf['model'])
        prompt = conf['prompt_template'].format(text=text)

        response = model.generate_content(
            prompt,
            generation_config=conf['generation_config']
        )
        
        raw_response_text = response.text

        # AIの応答からJSON部分を抽出する
        match = re.search(r"```(json)?\n?([\s\S]*?)\n?```", raw_response_text)
        if match:
            json_str = match.group(2)
        else:
            json_str = raw_response_text

        corrections = json.loads(json_str)
        
    except KeyError as e:
        print(f"Configuration error: Missing key {e} in 'proofread' config.")
        return {"corrections": []}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API response: {e}")
        return {"corrections": []}
    except Exception as e:
        print(f"An error occurred during proofreading: {e}")
        return {"corrections": []}

    return {"corrections": corrections}

