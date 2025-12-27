# Project Context: Streamlit Data Processing App

## Project Overview
- PythonベースのStreamlitフレームワークを用いた、データ分析・可視化アプリケーション。
- 大規模なデータセット（CSV/Excel/Parquet）を読み込み、クレンジング、統計解析、チャート表示を行う。

## Tech Stack
- Language: Python 3.10+
- Framework: Streamlit
- Data Manipulation: Pandas (or Polars)
- Visualization: Plotly, Matplotlib
- Environment: uv / venv / pip

## Streamlit Best Practices
- **Caching**: 重い処理（データ読み込み、重い計算）には必ず `@st.cache_data` を使用せよ。DB接続やモデルのロードには `@st.cache_resource` を使用せよ。
- **Session State**: ユーザー入力やページを跨ぐ状態保持には `st.session_state` を適切に使用せよ。
- **Layout**: `st.sidebar` を活用して設定項目を分離し、`st.columns` や `st.tabs` で画面を整理せよ。
- **Form**: 複数の入力項目がある場合は `st.form` を使い、送信ボタンが押されるまで再実行を抑制せよ。

## Coding Standards
- **Modularization**: `main.py` に全てを書かず、ロジックは `utils/` や `logic/` ディレクトリに分離せよ。
- **Type Hinting**: 関数の引数と戻り値には必ず型ヒントを付けること。
- **Docstrings**: 複雑なロジックには Google Style の docstring を記述せよ。
- **Error Handling**: データ読み込み失敗時などは `st.error` や `st.exception` を使ってユーザーに分かりやすく通知せよ。

## Specific Rules for Streamlit
- スクリプトが先頭から再実行されることを意識したコードを書くこと。
- 回答の中で `st.experimental_...` 系の非推奨APIは使わず、最新の安定版API（例: `st.cache_data`）を使用せよ。
- プロットを表示する際は `st.pyplot(fig)` よりも、インタラクティブな `st.plotly_chart(fig, use_container_width=True)` を優先せよ。

## Prohibited Patterns
- **Global Variables**: グローバル変数による状態管理は禁止（Streamlitでは機能しないため）。必ず `st.session_state` を使うこと。
- **Infinite Loops**: `while True` などの無限ループは Streamlit の実行モデルを破壊するため禁止。
- **Heavy Operations in UI**: UIのレンダリングループ内にキャッシュされていない重い処理を記述しないこと。

## Response Instructions
- 回答と解説は日本語で行うこと。
- コードを提示する際は、そのコードをどこ（どのファイル）に記述すべきか明記すること。
- Streamlitの再実行モデル（Rerun）を考慮した、効率的なコードを提案すること。
