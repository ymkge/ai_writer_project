# AIライティング支援ツール

Gemini APIを活用して、文章の要約と校正を行うWebアプリケーションです。

## ✨ 機能

- **文章要約**: 入力されたテキストを簡潔に要約します。
- **文章校正**: 誤字脱字や不自然な表現を検出し、修正案と理由を提示します。
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
└── frontend/         # Reactフロントエンドプロジェクト
    ├── src/
    ├── public/
    └── package.json
```

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