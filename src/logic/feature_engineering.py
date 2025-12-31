"""
feature_engineering.py
列演算、エンコーディング、スケーリング、日付特徴量抽出
"""
from typing import Optional, List
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, MinMaxScaler
import numpy as np
from src.utils.logger import get_logger
try:
    import streamlit as st
    _session_uid = st.session_state.get('session_uid') if hasattr(st, 'session_state') else None
except Exception:
    _session_uid = None

logger = get_logger(__name__, session_uid=_session_uid)

def add_column_by_operation(df: pd.DataFrame, col1: str, col2: Optional[str], op: str, const: Optional[float] = None) -> pd.DataFrame:
    """列同士または定数による新規列生成"""
    df = df.copy()
    if op == '加算':
        df[f'{col1}_plus_{col2}'] = df[col1] + df[col2]
    elif op == '減算':
        df[f'{col1}_minus_{col2}'] = df[col1] - df[col2]
    elif op == '乗算':
        df[f'{col1}_mul_{col2}'] = df[col1] * df[col2]
    elif op == '除算':
        df[f'{col1}_div_{col2}'] = df[col1] / df[col2]
    elif op == '定数加算' and const is not None:
        df[f'{col1}_plus_{const}'] = df[col1] + const
    return df

def one_hot_encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """One-Hot Encoding"""
    logger.info("one_hot_encode: column=%s", column)
    return pd.get_dummies(df, columns=[column], drop_first=False)

def label_encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Label Encoding"""
    df = df.copy()
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))
    logger.info("label_encode: column=%s classes=%s", column, getattr(le, 'classes_', None))
    return df

def standard_scale(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """標準化（StandardScaler）"""
    df = df.copy()
    scaler = StandardScaler()
    df[column] = scaler.fit_transform(df[[column]])
    logger.info("standard_scale: column=%s mean=%s std=%s", column, float(scaler.mean_[0]) if hasattr(scaler, 'mean_') else None, float(scaler.scale_[0]) if hasattr(scaler, 'scale_') else None)
    return df

def minmax_scale(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """正規化（MinMaxScaler）"""
    df = df.copy()
    scaler = MinMaxScaler()
    df[column] = scaler.fit_transform(df[[column]])
    logger.info("minmax_scale: column=%s data_min=%s data_max=%s", column, float(scaler.data_min_[0]) if hasattr(scaler, 'data_min_') else None, float(scaler.data_max_[0]) if hasattr(scaler, 'data_max_') else None)
    return df

def extract_date_features(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """日付型から年・月・曜日・休日フラグを抽出"""
    df = df.copy()
    df[f'{column}_year'] = pd.to_datetime(df[column], errors='coerce').dt.year
    df[f'{column}_month'] = pd.to_datetime(df[column], errors='coerce').dt.month
    df[f'{column}_weekday'] = pd.to_datetime(df[column], errors='coerce').dt.weekday
    df[f'{column}_is_holiday'] = pd.to_datetime(df[column], errors='coerce').dt.weekday >= 5
    logger.info("extract_date_features: column=%s", column)
    return df
