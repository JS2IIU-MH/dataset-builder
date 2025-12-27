"""
data_io.py
データ入出力（CSV/Parquet読込・書出し）、プレビュー生成ロジック
"""
from typing import Optional, Tuple, List
import pandas as pd
import streamlit as st
import io

@st.cache_data
def load_csv(file: io.BytesIO, encoding: Optional[str] = None, use_header: bool = True,
             column_names: Optional[List[str]] = None, header: Optional[int] = 0) -> pd.DataFrame:
    """CSVファイルをDataFrameとして読み込む
    Args:
        file: アップロードされたファイルオブジェクト
        encoding: 文字コード（省略時は自動判定）
        use_header: 古い呼び出しで使われる場合のフラグ（Trueなら先頭行をヘッダとして扱う）
        column_names: 手動で与えられた列名リスト（与えられた場合は header=None, names=column_names で読み込む）
        header: 互換性のため既存コードで渡される keyword 引数（0 または None）。
                優先順位: `column_names` -> `header` -> `use_header` の順で解釈される。
    Returns:
        DataFrame
    """
    if column_names is not None:
        return pd.read_csv(file, encoding=encoding, header=None, names=column_names)

    # 既存コードが header キーワードで渡すことを許容する（例: header=None）
    if header is not None:
        return pd.read_csv(file, encoding=encoding, header=header)

    header_val = 0 if use_header else None
    return pd.read_csv(file, encoding=encoding, header=header_val)

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
