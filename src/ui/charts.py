"""
charts.py
EDA用グラフ（ヒストグラム・箱ひげ図・相関ヒートマップ等）
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def plot_histogram(df: pd.DataFrame, column: str):
    fig = px.histogram(df, x=column, nbins=30, title=f"ヒストグラム: {column}")
    st.plotly_chart(fig, width='stretch')

def plot_box(df: pd.DataFrame, column: str):
    fig = px.box(df, y=column, title=f"箱ひげ図: {column}")
    st.plotly_chart(fig, width='stretch')

def plot_corr_heatmap(corr_df: pd.DataFrame):
    fig = px.imshow(corr_df, text_auto=True, color_continuous_scale='RdBu', title="相関ヒートマップ")
    st.plotly_chart(fig, width='stretch')
