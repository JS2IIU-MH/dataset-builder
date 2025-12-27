"""
feature_engineering.py
列演算、エンコーディング、スケーリング、日付特徴量抽出
"""
from typing import Optional, List
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, MinMaxScaler
import numpy as np

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
    return pd.get_dummies(df, columns=[column], drop_first=False)

def label_encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Label Encoding"""
    df = df.copy()
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))
    return df

def standard_scale(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """標準化（StandardScaler）"""
    df = df.copy()
    scaler = StandardScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

def minmax_scale(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """正規化（MinMaxScaler）"""
    df = df.copy()
    scaler = MinMaxScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

def extract_date_features(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """日付型から年・月・曜日・休日フラグを抽出"""
    df = df.copy()
    df[f'{column}_year'] = pd.to_datetime(df[column], errors='coerce').dt.year
    df[f'{column}_month'] = pd.to_datetime(df[column], errors='coerce').dt.month
    df[f'{column}_weekday'] = pd.to_datetime(df[column], errors='coerce').dt.weekday
    df[f'{column}_is_holiday'] = pd.to_datetime(df[column], errors='coerce').dt.weekday >= 5
    return df
