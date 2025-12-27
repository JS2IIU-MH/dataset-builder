"""
eda.py
基本統計量、欠損値・分布・相関分析等のEDA処理
"""
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np

def describe_basic(df: pd.DataFrame) -> pd.DataFrame:
    """基本統計量（describe相当）を返す"""
    return df.describe(include='all').T

def missing_info(df: pd.DataFrame) -> pd.DataFrame:
    """各列の欠損数・欠損率を返す"""
    total = df.isnull().sum()
    percent = df.isnull().mean() * 100
    return pd.DataFrame({'欠損数': total, '欠損率(%)': percent})

def corr_matrix(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """相関係数行列を返す"""
    num_df = df.select_dtypes(include="number")
    return num_df.corr(method=method)
