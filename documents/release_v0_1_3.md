# Release v0.1.3

> リリース: v0.1.3
>
> コミット: 5691bb983883bb06cfebc59cd4c2cf932579fb54
> 日付: 2026-02-28

## 概要

v0.1.3 は「列の順序変更（ドラッグ&ドロップ）」機能を追加したマイナーリリースです。データプレビュータブ上で列の並び順を直感的に操作できるようになり、前処理ワークフローの利便性が向上しました。また、週次リポジトリステータスレポート自動生成ワークフローを追加しています。

## ハイライト

- **列の順序変更（ドラッグ&ドロップ）**: `streamlit-sortables` ライブラリを導入し、データプレビュータブ上でドラッグ&ドロップによる列の並び替えが可能になりました。変更前後のプレビューを確認したうえで「列の順序を適用」ボタンで確定できます。
- **`reorder_columns()` 関数の追加**: `src/logic/data_io.py` に列順序変更ロジックを実装しました。新しい順序に含まれない列は末尾に自動追加されます。
- **`render_column_reorder()` UI コンポーネントの追加**: `src/ui/forms.py` にドラッグ&ドロップ UI を実装し、`main.py` のデータプレビュータブに統合しました。
- **週次リポジトリステータスレポート**: GitHub Actions ワークフローを追加し、リポジトリの週次サマリを自動生成する仕組みを導入しました。

## 変更ファイル（主なもの）

- [`requirements.txt`](requirements.txt) — `streamlit-sortables` を追加
- [`src/logic/data_io.py`](src/logic/data_io.py) — `reorder_columns()` 関数の追加
- [`src/ui/forms.py`](src/ui/forms.py) — `render_column_reorder()` UI コンポーネントの追加
- [`main.py`](main.py) — データプレビュータブへの列順序変更機能の統合
- [`documents/requirements.md`](documents/requirements.md) — 列の順序変更要件を追加

## 依存関係の更新

- 追加: `streamlit-sortables`（最新版）

## バグ修正 / 安定化

- 特になし（本リリースは新機能追加が中心です）

## アップグレード/移行手順

特別な移行手順は不要です。依存関係を更新して通常通り起動してください。

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

## 既知の制限

- 特になし

## 今後の予定

- 列のフィルタリング機能
- 列の一括選択・解除機能
- ドラッグ&ドロップによる列の削除機能
