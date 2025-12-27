"""
export.py
コード出力・データエクスポートUI
"""
import streamlit as st
from src.logic import data_io

def code_export_area(code: str):
    st.subheader("Pandasコード出力")
    st.code(code, language="python")


def data_export_area(df):
    st.subheader("最終データのダウンロード")

    # 最終データのプレビュー
    st.subheader("最終データのプレビュー")
    try:
        preview_n = st.number_input("表示する行数", min_value=1, max_value=100, value=5, key="export_preview_n")
        st.dataframe(df.head(int(preview_n)))
    except Exception:
        st.info("プレビューを表示できませんでした")

    try:
        csv_bytes = data_io.export_csv(df)
        st.download_button("CSVダウンロード", csv_bytes, file_name="final.csv", mime="text/csv")
    except Exception:
        # フォールバック: 互換性のため従来のエンコードでも提供
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("CSVダウンロード", csv, file_name="final.csv", mime="text/csv")

    try:
        import io
        buf = io.BytesIO()
        df.to_parquet(buf, index=False)
        st.download_button("Parquetダウンロード", buf.getvalue(), file_name="final.parquet", mime="application/octet-stream")
    except Exception:
        st.info("pyarrow等が未インストールの場合はParquet出力不可")
