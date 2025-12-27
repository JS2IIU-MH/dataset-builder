"""
forms.py
クリーニング・特徴量エンジニアリング用フォームUI
"""
import streamlit as st
from typing import List


def cleaning_form(df, num_cols: List[str], obj_cols: List[str], cat_cols: List[str], date_cols: List[str]):
    st.subheader("型変換")
    col = st.selectbox("型変換する列を選択", df.columns, key="clean_dtype_col")
    dtype = st.selectbox("変換後の型", ["数値", "文字列", "カテゴリ", "日付"], key="clean_dtype_type")
    if st.button("型変換実行", key="clean_dtype_btn"):
        st.session_state['df'] = st.session_state['cleaning'].convert_dtype(st.session_state['df'], col, dtype)
        st.success(f"{col} を {dtype} に変換しました")

    st.subheader("欠損値処理")
    col2 = st.selectbox("欠損値処理する列を選択", df.columns, key="clean_na_col")
    method = st.selectbox("処理方法", ["削除(行)", "削除(列)", "平均", "中央値", "最頻値", "定数"], key="clean_na_method")
    value = None
    if method == "定数":
        value = st.text_input("補完値を入力", key="clean_na_value")
    if st.button("欠損値処理実行", key="clean_na_btn"):
        if method == "削除(行)":
            st.session_state['df'] = st.session_state['cleaning'].drop_missing(st.session_state['df'], axis=0)
        elif method == "削除(列)":
            st.session_state['df'] = st.session_state['cleaning'].drop_missing(st.session_state['df'], axis=1)
        else:
            m = method if method != "定数" else "定数"
            st.session_state['df'] = st.session_state['cleaning'].fill_missing(st.session_state['df'], col2, m, value)
        st.success("欠損値処理を実行しました")

    st.subheader("重複削除")
    if st.button("重複行を削除", key="clean_dup_btn"):
        st.session_state['df'] = st.session_state['cleaning'].drop_duplicates(st.session_state['df'])
        st.success("重複行を削除しました")

    st.subheader("外れ値処理")
    col3 = st.selectbox("外れ値処理する数値列を選択", num_cols, key="clean_outlier_col")
    method2 = st.selectbox("外れ値処理方法", ["IQRクリッピング", "3σ削除"], key="clean_outlier_method")
    if st.button("外れ値処理実行", key="clean_outlier_btn"):
        if method2 == "IQRクリッピング":
            st.session_state['df'] = st.session_state['cleaning'].clip_outliers_iqr(st.session_state['df'], col3)
        else:
            st.session_state['df'] = st.session_state['cleaning'].remove_outliers_sigma(st.session_state['df'], col3)
        st.success("外れ値処理を実行しました")


def feature_engineering_form(df, num_cols: List[str], obj_cols: List[str], cat_cols: List[str], date_cols: List[str]):
    st.subheader("新規列生成（演算）")
    col1 = st.selectbox("演算元の列", num_cols, key="fe_op_col1")
    op = st.selectbox("演算種別", ["加算", "減算", "乗算", "除算", "定数加算"], key="fe_op_type")
    col2 = None
    const = None
    if op in ["加算", "減算", "乗算", "除算"]:
        col2 = st.selectbox("演算対象の列", num_cols, key="fe_op_col2")
    elif op == "定数加算":
        const = st.number_input("加算する定数", value=0.0, key="fe_op_const")
    if st.button("新規列生成", key="fe_op_btn"):
        st.session_state['df'] = st.session_state['feature'].add_column_by_operation(st.session_state['df'], col1, col2, op, const)
        st.success("新規列を生成しました")

    st.subheader("エンコーディング")
    col3 = st.selectbox("エンコーディングする列", cat_cols + obj_cols, key="fe_enc_col")
    enc_method = st.selectbox("エンコーディング手法", ["One-Hot", "Label"], key="fe_enc_method")
    if st.button("エンコーディング実行", key="fe_enc_btn"):
        if enc_method == "One-Hot":
            st.session_state['df'] = st.session_state['feature'].one_hot_encode(st.session_state['df'], col3)
        else:
            st.session_state['df'] = st.session_state['feature'].label_encode(st.session_state['df'], col3)
        st.success("エンコーディングを実行しました")

    st.subheader("スケーリング")
    col4 = st.selectbox("スケーリングする数値列", num_cols, key="fe_scale_col")
    scale_method = st.selectbox("スケーリング手法", ["StandardScaler", "MinMaxScaler"], key="fe_scale_method")
    if st.button("スケーリング実行", key="fe_scale_btn"):
        if scale_method == "StandardScaler":
            st.session_state['df'] = st.session_state['feature'].standard_scale(st.session_state['df'], col4)
        else:
            st.session_state['df'] = st.session_state['feature'].minmax_scale(st.session_state['df'], col4)
        st.success("スケーリングを実行しました")

    st.subheader("日付特徴量抽出")
    if date_cols:
        col5 = st.selectbox("日付特徴量を抽出する列", date_cols, key="fe_date_col")
        if st.button("日付特徴量抽出実行", key="fe_date_btn"):
            st.session_state['df'] = st.session_state['feature'].extract_date_features(st.session_state['df'], col5)
            st.success("日付特徴量を抽出しました")
