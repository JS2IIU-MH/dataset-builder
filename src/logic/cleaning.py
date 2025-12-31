"""
cleaning.py
型変換、欠損値・重複・外れ値処理
"""
from typing import Optional, Any
import pandas as pd
import numpy as np
from src.utils.logger import get_logger
try:
    import streamlit as st
    _session_uid = st.session_state.get('session_uid') if hasattr(st, 'session_state') else None
except Exception:
    _session_uid = None

logger = get_logger(__name__, session_uid=_session_uid)

def convert_dtype(df: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    """指定列の型変換"""
    df = df.copy()
    if dtype == '数値':
        df[column] = pd.to_numeric(df[column], errors='coerce')
    elif dtype == '文字列':
        df[column] = df[column].astype(str)
    elif dtype == 'カテゴリ':
        df[column] = df[column].astype('category')
    elif dtype == '日付':
        df[column] = pd.to_datetime(df[column], errors='coerce')
    try:
        logger.info("convert_dtype: column=%s dtype=%s", column, dtype)
    except Exception:
        pass
    return df

def drop_missing(df: pd.DataFrame, axis: int = 0) -> pd.DataFrame:
    """欠損値を含む行または列を削除"""
    logger.info("drop_missing: axis=%s before_rows=%d", axis, df.shape[0])
    res = df.dropna(axis=axis)
    logger.info("drop_missing: after_rows=%d", res.shape[0])
    return res

def fill_missing(df: pd.DataFrame, column: str, method: str, value: Optional[Any] = None) -> pd.DataFrame:
    """欠損値を指定方法で補完"""
    df = df.copy()
    if method == '平均':
        df[column] = df[column].fillna(df[column].mean())
    elif method == '中央値':
        df[column] = df[column].fillna(df[column].median())
    elif method == '最頻値':
        df[column] = df[column].fillna(df[column].mode().iloc[0])
    elif method == '定数' and value is not None:
        df[column] = df[column].fillna(value)
    logger.info("fill_missing: column=%s method=%s", column, method)
    return df

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """重複行を削除"""
    logger.info("drop_duplicates: before_rows=%d", df.shape[0])
    res = df.drop_duplicates()
    logger.info("drop_duplicates: after_rows=%d", res.shape[0])
    return res

def clip_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """IQR法で外れ値を上下限でクリッピング"""
    df = df.copy()
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    df[column] = df[column].clip(lower, upper)
    logger.info("clip_outliers_iqr: column=%s lower=%s upper=%s", column, lower, upper)
    return df

def remove_outliers_sigma(df: pd.DataFrame, column: str, sigma: float = 3.0) -> pd.DataFrame:
    """3σ法で外れ値行を削除"""
    mean = df[column].mean()
    std = df[column].std()
    lower = mean - sigma * std
    upper = mean + sigma * std
    logger.info("remove_outliers_sigma: column=%s mean=%s std=%s sigma=%s lower=%s upper=%s", column, mean, std, sigma, lower, upper)
    return df[(df[column] >= lower) & (df[column] <= upper)]
