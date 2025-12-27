"""
data_io.py
データ入出力（CSV/Parquet読込・書出し）、プレビュー生成ロジック
"""
from typing import Optional, Tuple
import pandas as pd
import streamlit as st
import io

@st.cache_data
def load_csv(file: io.BytesIO, encoding: Optional[str] = None, header: Optional[int] = 0) -> pd.DataFrame:
    """CSVファイルをDataFrameとして読み込む
    Args:
        file: アップロードされたファイルオブジェクト
        encoding: 文字コード（省略時は自動判定）
        header: 先頭行をヘッダーとして扱う場合は0、データとして扱う場合はNone
    Returns:
        DataFrame
    """
    return pd.read_csv(file, encoding=encoding, header=header)

@st.cache_data
def load_parquet(file: io.BytesIO) -> pd.DataFrame:
    """ParquetファイルをDataFrameとして読み込む"""
    return pd.read_parquet(file)

@st.cache_data
def preview_df(df: pd.DataFrame, head: int = 5, tail: int = 0) -> pd.DataFrame:
    """DataFrameの先頭・末尾プレビューを返す"""
    if tail > 0:
        return pd.concat([df.head(head), df.tail(tail)])
    return df.head(head)

def export_csv(df: pd.DataFrame) -> bytes:
    """DataFrameをCSVバイト列に変換"""
    return df.to_csv(index=False).encode('utf-8')

def export_parquet(df: pd.DataFrame) -> bytes:
    """DataFrameをParquetバイト列に変換"""
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    return buf.getvalue()
