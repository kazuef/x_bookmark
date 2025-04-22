# X Bookmark Categorizer

## 概要

このプロジェクトは、X のブックマークを自動的にカテゴリ分類し、SQLite データベースに保存する API を提供します。

## 機能

- ブックマークの JSON ファイルをアップロードして自動カテゴリ分類
- 分類されたブックマークを SQLite データベースに永続化
- カテゴリ一覧の取得
- カテゴリ別ブックマークの取得

## 技術スタック

- FastAPI: Web フレームワーク
- SQLite3: データベース
- Dify: 自然言語処理によるカテゴリ分類

## セットアップ

### 前提条件

- Python 3.8 以上
- Poetry（依存関係管理）

### インストール

```bash
# リポジトリをクローン
git clone <repository-url>
cd scan_receipt

# 依存関係のインストール
poetry install
```

### 環境変数の設定

`env/.env`ファイルを作成し、以下の内容を設定してください：

```
DIFY_API_KEY=your_dify_api_key
```

### データベースの初期化

アプリケーションの初回起動時に自動的にデータベースが初期化されます。手動で初期化する場合は以下のコマンドを実行してください：

```python
from bookmarks_categorize.modules.database import init_db
init_db()
```

## 使用方法

### サーバーの起動

main.py が配置されている階層(bookmarks_categorize)で以下コマンドを実行してください：

```bash
poetry run uvicorn bookmarks_categorize.main:app --reload
```

### API エンドポイント

#### ブックマークのカテゴリ分類と保存

```
POST /bookmarks/categorize
```

リクエスト: マルチパートフォームデータで JSON ファイルをアップロード

レスポンス: カテゴリ分類されたブックマークのリスト

#### カテゴリ一覧の取得

```
GET /bookmarks/categories
```

レスポンス: 登録されているカテゴリの一覧

#### ブックマークの取得

```
GET /bookmarks/bookmarks?category_id={category_id}
```

パラメータ:

- `category_id`: (オプション) 特定のカテゴリのブックマークのみを取得する場合に指定

レスポンス: ブックマークのリスト

## データベース構造

### bookmarks_category テーブル

- `id`: カテゴリ ID (主キー)
- `categorize_name`: カテゴリ名 (一意)
- `created_at`: 作成日時
- `updated_at`: 更新日時
- `is_deleted`: 論理削除フラグ

### bookmarks テーブル

- `id`: ブックマーク ID (主キー)
- `categorize_id`: カテゴリ ID (外部キー)
- `tweet`: ツイート内容 (JSON)
- `created_at`: 作成日時
- `updated_at`: 更新日時
- `is_deleted`: 論理削除フラグ
