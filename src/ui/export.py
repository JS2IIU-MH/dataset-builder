"""
export.py
コード出力・データエクスポートUI
"""
import streamlit as st

def code_export_area(code: str):
    st.subheader("Pandasコード出力")
    st.code(code, language="python")

def data_export_area(df):
    st.subheader("最終データのダウンロード")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("CSVダウンロード", csv, file_name="final.csv", mime="text/csv")
    try:
        import io
        buf = io.BytesIO()
        df.to_parquet(buf, index=False)
        st.download_button("Parquetダウンロード", buf.getvalue(), file_name="final.parquet", mime="application/octet-stream")
    except Exception:
        st.info("pyarrow等が未インストールの場合はParquet出力不可")
