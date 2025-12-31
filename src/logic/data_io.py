"""
data_io.py
データ入出力（CSV/Parquet読込・書出し）、プレビュー生成ロジック
"""
from typing import Optional, Tuple, List
import pandas as pd
import streamlit as st
import io
import hashlib
from src.utils.logger import get_logger

def _compute_sha256(data: bytes) -> str:
    """バイト列の SHA256 チェックサムを返す"""
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


@st.cache_data
def _load_csv_from_bytes(file_bytes: bytes, checksum: str, session_id: str,
                         encoding: Optional[str] = None,
                         use_header: bool = True, column_names: Optional[List[str]] = None,
                         header: Optional[int] = 0) -> pd.DataFrame:
    """内部キャッシュ関数: バイト列とチェックサムを受け取り DataFrame を返す
    キャッシュキーに `checksum` を含めることで、ファイル内容ベースでの分離を保証する。
    """
    buf = io.BytesIO(file_bytes)
    if column_names is not None:
        return pd.read_csv(buf, encoding=encoding, header=None, names=column_names)

    if header is not None:
        return pd.read_csv(buf, encoding=encoding, header=header)

    header_val = 0 if use_header else None
    return pd.read_csv(buf, encoding=encoding, header=header_val)


def load_csv(file: io.BytesIO, encoding: Optional[str] = None, use_header: bool = True,
             column_names: Optional[List[str]] = None, header: Optional[int] = 0,
             session_id: Optional[str] = None) -> pd.DataFrame:
    """CSVファイルをDataFrameとして読み込む（UploadedFile 等をバイト列に変換して内部でキャッシュを行う）
    Args:
        file: アップロードされたファイルオブジェクト（または bytes）
        encoding: 文字コード
        use_header: 先頭行をヘッダとして扱うか
        column_names: 明示的な列名
        header: header 引数（互換性のため）
    Returns:
        DataFrame
    """
    # `file` が UploadedFile や BytesIO の場合はバイト列に変換してから
    # 内部のキャッシュ対応関数を呼ぶ。バイト列の SHA256 をキャッシュキーに使う。
    if hasattr(file, 'seek'):
        try:
            file.seek(0)
        except Exception:
            pass
    if hasattr(file, 'read'):
        file_bytes = file.read()
    elif isinstance(file, (bytes, bytearray)):
        file_bytes = bytes(file)
    else:
        raise TypeError('file must be a file-like object or bytes')

    checksum = _compute_sha256(file_bytes)
    sid = session_id or ''
    df = _load_csv_from_bytes(file_bytes, checksum, sid, encoding=encoding,
                                use_header=use_header, column_names=column_names, header=header)
    logger = get_logger(__name__, session_uid=sid)
    try:
        logger.info("load_csv: file_bytes=%d checksum=%s rows=%d cols=%d", len(file_bytes), checksum, df.shape[0], df.shape[1])
    except Exception:
        logger.info("load_csv: file_bytes=%d checksum=%s", len(file_bytes), checksum)
    return df

@st.cache_data
def _load_parquet_from_bytes(file_bytes: bytes, checksum: str, session_id: str) -> pd.DataFrame:
    """内部キャッシュ関数: Parquet のバイト列から DataFrame を読み込む"""
    buf = io.BytesIO(file_bytes)
    return pd.read_parquet(buf)


def load_parquet(file: io.BytesIO, session_id: Optional[str] = None) -> pd.DataFrame:
    """ParquetファイルをDataFrameとして読み込む（アップロードオブジェクトはバイト列に変換して扱う）"""
    if hasattr(file, 'seek'):
        try:
            file.seek(0)
        except Exception:
            pass
    if hasattr(file, 'read'):
        file_bytes = file.read()
    elif isinstance(file, (bytes, bytearray)):
        file_bytes = bytes(file)
    else:
        raise TypeError('file must be a file-like object or bytes')

    checksum = _compute_sha256(file_bytes)
    sid = session_id or ''
    df = _load_parquet_from_bytes(file_bytes, checksum, sid)
    logger = get_logger(__name__, session_uid=sid)
    try:
        logger.info("load_parquet: bytes=%d checksum=%s rows=%d cols=%d", len(file_bytes), checksum, df.shape[0], df.shape[1])
    except Exception:
        logger.info("load_parquet: bytes=%d checksum=%s", len(file_bytes), checksum)
    return df

@st.cache_data
def preview_df(df: pd.DataFrame, head: int = 5, tail: int = 0) -> pd.DataFrame:
    """DataFrameの先頭・末尾プレビューを返す"""
    if tail > 0:
        return pd.concat([df.head(head), df.tail(tail)])
    return df.head(head)

def export_csv(df: pd.DataFrame) -> bytes:
    """DataFrameをCSVバイト列に変換"""
    # 明示的にヘッダーを有効にし、Excelでの文字化け対策として UTF-8 with BOM を使う
    df2 = df.copy()
    # カラム名が数値等の場合でも文字列にしてヘッダ行として出力されるようにする
    df2.columns = [str(c) for c in df2.columns]
    return df2.to_csv(index=False, header=True).encode('utf-8-sig')

def export_parquet(df: pd.DataFrame) -> bytes:
    """DataFrameをParquetバイト列に変換"""
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    return buf.getvalue()
