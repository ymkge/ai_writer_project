# AIライティング支援ツール
<img width="1707" height="699" alt="スクリーンショット 2025-08-28 21 38 52" src="https://github.com/user-attachments/assets/07f00217-2bbd-40c3-bdf0-f0ba0e49bc2f" />

Gemini APIを活用して、文章の要約と校正を行うWebアプリケーションです。

## ✨ 機能

- **文章要約**: 入力されたテキストを簡潔に要約します。
- **文章校正**: 誤字脱字や不自然な表現を検出し、修正案と理由を提示します。
- **結果のCSVダウンロード**: 要約結果と校正結果をフロントエンドからCSVファイルとしてダウンロードできます。（校正結果は、元文章が重複しないように最適化されています。）
- **Web API**: FastAPIで構築されたバックエンドAPI。
- **Web UI**: ReactとMaterial-UIで構築された、モダンでリッチなユーザーインターフェース。

## 🛠️ 技術スタック

- **バックエンド**: Python, FastAPI, Uvicorn, python-dotenv
- **フロントエンド**: React, Material-UI (MUI), Axios
- **AIモデル**: Google Gemini (gemini-2.5-flash)

## 📂 プロジェクト構成

```
/ai_writer_project/
├── core.py           # Geminiとの連携などコアロジック
├── main.py           # FastAPIアプリケーション (APIエンドポイント)
├── requirements.txt  # Pythonの依存ライブラリ
├── .env.example      # 環境変数のサンプルファイル
├── .gitignore        # Gitの無視ファイル設定
├── README.md         # このファイル
├── prompt_config.json # プロンプトとモデルの設定ファイル
└── frontend/         # Reactフロントエンドプロジェクト
    ├── src/
    ├── public/
    └── package.json
## ⚙️ 設定ファイル

AIモデルの挙動（プロンプト、モデル名、生成パラメータなど）は、`prompt_config.json`ファイルで設定できます。

- `prompt_config.json`: 要約機能と校正機能のプロンプトテンプレート、使用するGeminiモデル、および`temperature`などの生成パラメータが定義されています。このファイルを編集することで、AIの応答を柔軟に調整できます。

**例:** `prompt_config.json`の一部

```json
{
  "summarize": {
    "model": "gemini-2.5-flash",
    "prompt_template": "以下の文章を簡潔に要約してください。\n\n---\n{text}\n---",
    "generation_config": {
      "temperature": 0.7,
      "top_p": 1,
      "max_output_tokens": 2048
    }
  },
  "proofread": {
    "model": "gemini-2.5-flash",
    "prompt_template": "あなたはプロの編集者です。以下の文章を校正し、修正点を指摘してください。\n...",
    "generation_config": {
      "response_mime_type": "application/json",
      "temperature": 0.2
    }
  }
}
```

**注意:** `prompt_config.json`を変更した際は、変更を反映させるためにFastAPIサーバーを再起動してください。

## 🚀 セットアップと実行方法


### 前提条件

- Python 3.8以上
- Node.js 16以上
- `pip` と `npm` がインストールされていること
- Gemini APIキー (Google AI Studio等で取得)

### 1. バックエンドのセットアップと起動

まず、APIサーバーを起動します。

```bash
# 1. プロジェクトのルートディレクトリに移動
cd /path/to/ai_writer_project

# 2. (推奨) Python仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# 3. 依存ライブラリをインストール
pip install -r requirements.txt

# 4. 環境変数ファイルを作成
# .env.exampleをコピーして.envファイルを作成します
cp .env.example .env

# 5. .envファイルにAPIキーを記述
# YOUR_API_KEY_HERE の部分を実際のキーに書き換えてください
nano .env  # もしくはお好みのエディタで編集

# 6. FastAPIサーバーを起動
uvicorn main:app --reload
```

サーバーが `http://127.0.0.1:8000` で起動します。

### 2. フロントエンドのセットアップと起動

次に、WebアプリケーションのUIを起動します。新しいターミナルを開いて実行してください。

```bash
# 1. フロントエンドのディレクトリに移動
cd /path/to/ai_writer_project/frontend

# 2. 依存ライブラリをインストール
npm install

# 3. React開発サーバーを起動
npm start
```

ブラウザが自動的に開き、 `http://localhost:3000` でアプリケーションが表示されます。
