# Dataset Builder

このリポジトリは、Streamlit を用いたデータ読み込み・前処理・可視化アプリケーションのサンプル実装です。

## 目的

- 大規模なCSV/Parquetデータを読み込み、クレンジング、簡易EDA、特徴量エンジニアリング、可視化、エクスポートを行うためのツール群を提供します。

## リポジトリ構成（抜粋）

- `main.py` — Streamlit アプリのエントリポイント
- `src/logic/` — データ処理ロジック（`data_io.py`, `cleaning.py`, `eda.py`, `feature_engineering.py`, `codegen.py`）
- `src/ui/` — UI コンポーネント（`charts.py`, `forms.py`, `sidebar.py`, `export.py`）
- `sample-data/` — サンプルデータ（例: `sample-data/iris/iris.csv`）
- `documents/architecture.md` — アーキテクチャ説明

## 要件

- Python 3.10+
- 依存関係は `requirements.txt` / `dev-requirements.txt` に記載

## セットアップ

1. 仮想環境を作成・有効化（例: `venv`）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 開発依存が必要な場合:

```bash
pip install -r dev-requirements.txt
```

## 実行（ローカル）

```bash
streamlit run main.py
```

## 主要な使い方

- サイドバーでデータファイルを選択・アップロードし、読み込み後にクレンジングやEDAタブで可視化・分析できます。
- 処理は重い計算やI/Oを `@st.cache_data` / `@st.cache_resource` でキャッシュする設計になっています（実装は `src/logic/` を参照）。

## 開発者向けメモ

- Streamlit の再実行モデルを考慮し、グローバル変数は使わず `st.session_state` を利用してください。
- 重い処理（ファイル読み込み、特徴量生成など）は `@st.cache_data` でキャッシュしてください。
- UI は `src/ui/` に分離しており、ロジックは `src/logic/` に置いてあります。変更は該当ファイルを編集してください。
- 詳細アーキテクチャは [documents/architecture.md](documents/architecture.md) を参照。

## サンプルデータ

- `sample-data/iris/iris.csv` を例にデータ構造や利用方法を確認できます。

## テスト

- 自動テストがある場合は `dev-requirements.txt` にテストランナーが含まれます。簡易的にはユニットテストを追加し、`pytest` 等で実行してください。

## 貢献

- Issue / PR を歓迎します。コーディング規約や命名規則は既存コードに合わせてください。

## ライセンス

- 本プロジェクトは `LICENSE` を参照してください。

## お問い合わせ

- 実装や設計に関する質問は Issue を立ててください。
