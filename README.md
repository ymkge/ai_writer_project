# AIライティング支援ツール

Gemini APIを活用して、文章の要約と校正を行うWebアプリケーションです。

## ✨ 機能

- **文章要約**: 入力されたテキストを簡潔に要約します。
- **文章校正**: 誤字脱字や不自然な表現を検出し、修正案と理由を提示します。
- **Web API**: FastAPIで構築されたバックエンドAPI。
- **Web UI**: ReactとBootstrapで構築された、直感的で使いやすいユーザーインターフェース。

## 🛠️ 技術スタック

- **バックエンド**: Python, FastAPI, Uvicorn
- **フロントエンド**: React, Bootstrap, Axios
- **AIモデル**: Google Gemini

## 📂 プロジェクト構成

```
/ai_writer_project/
├── core.py           # Geminiとの連携などコアロジック
├── main.py           # FastAPIアプリケーション (APIエンドポイント)
├── cli.py            # (オプション) CLIツール
├── requirements.txt  # Pythonの依存ライブラリ
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

### 1. バックエンドのセットアップと起動

まず、APIサーバーを起動します。

```bash
# プロジェクトのルートディレクトリに移動
cd /path/to/ai_writer_project

# 依存ライブラリをインストール
# (注: Gemini APIキーをcore.pyに設定する必要があります)
pip install -r requirements.txt

# FastAPIサーバーを起動
uvicorn main:app --reload
```

サーバーが `http://127.0.0.1:8000` で起動します。

### 2. フロントエンドのセットアップと起動

次に、WebアプリケーションのUIを起動します。新しいターミナルを開いて実行してください。

```bash
# フロントエンドのディレクトリに移動
cd /path/to/ai_writer_project/frontend

# 依存ライブラリをインストール
npm install

# React開発サーバーを起動
npm start
```

ブラウザが自動的に開き、 `http://localhost:3000` でアプリケーションが表示されます。
