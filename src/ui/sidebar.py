"""
sidebar.py
サイドバーUI（ファイルアップロード、データサイズ表示、リセット・ダウンロードボタン）
"""
import streamlit as st
from typing import Optional

def sidebar_file_uploader() -> Optional[bytes]:
    """CSV/ParquetファイルアップロードUI"""
    uploaded = st.sidebar.file_uploader(
        'データファイルをアップロード (CSV/Parquet)',
        type=['csv', 'parquet']
    )
    # 先頭行を列名として扱うかどうかのチェックボックス
    st.sidebar.markdown('---')
    st.sidebar.checkbox('先頭行を列名（ヘッダー）として扱う', value=True, key='use_header')
    return uploaded

def sidebar_data_shape(df):
    """データサイズ（行・列）表示"""
    if df is not None:
        st.sidebar.info(f"データサイズ: {df.shape[0]} 行 × {df.shape[1]} 列")

def sidebar_reset_button() -> bool:
    """リセットボタン"""
    return st.sidebar.button('リセット', key='reset_btn')

def sidebar_download_button(label: str, data: bytes, file_name: str, mime: str):
    """ダウンロードボタン"""
    st.sidebar.download_button(
        label=label,
        data=data,
        file_name=file_name,
        mime=mime
    )
