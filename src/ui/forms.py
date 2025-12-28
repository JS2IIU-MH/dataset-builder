"""
forms.py
クリーニング・特徴量エンジニアリング用フォームUI
"""
import streamlit as st
from typing import List
import pandas as pd
import re


def cleaning_form(df, num_cols: List[str], obj_cols: List[str], cat_cols: List[str], date_cols: List[str]):
    st.subheader("型変換")
    col = st.selectbox("型変換する列を選択", df.columns, key="clean_dtype_col")
    dtype = st.selectbox("変換後の型", ["数値", "文字列", "カテゴリ", "日付"], key="clean_dtype_type")
    if st.button("型変換実行", key="clean_dtype_btn"):
        import src.logic.cleaning as cleaning
        st.session_state['df'] = cleaning.convert_dtype(st.session_state['df'], col, dtype)
        st.success(f"{col} を {dtype} に変換しました")

    st.subheader("欠損値処理")
    col2 = st.selectbox("欠損値処理する列を選択", df.columns, key="clean_na_col")
    method = st.selectbox("処理方法", ["削除(行)", "削除(列)", "平均", "中央値", "最頻値", "定数"], key="clean_na_method")
    value = None
    if method == "定数":
        value = st.text_input("補完値を入力", key="clean_na_value")
    if st.button("欠損値処理実行", key="clean_na_btn"):
        import src.logic.cleaning as cleaning
        if method == "削除(行)":
            st.session_state['df'] = cleaning.drop_missing(st.session_state['df'], axis=0)
        elif method == "削除(列)":
            st.session_state['df'] = cleaning.drop_missing(st.session_state['df'], axis=1)
        else:
            m = method if method != "定数" else "定数"
            st.session_state['df'] = cleaning.fill_missing(st.session_state['df'], col2, m, value)
        st.success("欠損値処理を実行しました")

    st.subheader("重複削除")
    if st.button("重複行を削除", key="clean_dup_btn"):
        import src.logic.cleaning as cleaning
        st.session_state['df'] = cleaning.drop_duplicates(st.session_state['df'])
        st.success("重複行を削除しました")

    st.subheader("外れ値処理")
    col3 = st.selectbox("外れ値処理する数値列を選択", num_cols, key="clean_outlier_col")
    method2 = st.selectbox("外れ値処理方法", ["IQRクリッピング", "3σ削除"], key="clean_outlier_method")
    if st.button("外れ値処理実行", key="clean_outlier_btn"):
        import src.logic.cleaning as cleaning
        if method2 == "IQRクリッピング":
            st.session_state['df'] = cleaning.clip_outliers_iqr(st.session_state['df'], col3)
        else:
            st.session_state['df'] = cleaning.remove_outliers_sigma(st.session_state['df'], col3)
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
        import src.logic.feature_engineering as feature
        st.session_state['df'] = feature.add_column_by_operation(st.session_state['df'], col1, col2, op, const)
        st.success("新規列を生成しました")

    st.subheader("エンコーディング")
    col3 = st.selectbox("エンコーディングする列", cat_cols + obj_cols, key="fe_enc_col")
    enc_method = st.selectbox("エンコーディング手法", ["One-Hot", "Label"], key="fe_enc_method")
    if st.button("エンコーディング実行", key="fe_enc_btn"):
        import src.logic.feature_engineering as feature
        if enc_method == "One-Hot":
            st.session_state['df'] = feature.one_hot_encode(st.session_state['df'], col3)
        else:
            st.session_state['df'] = feature.label_encode(st.session_state['df'], col3)
        st.success("エンコーディングを実行しました")

    st.subheader("スケーリング")
    col4 = st.selectbox("スケーリングする数値列", num_cols, key="fe_scale_col")
    scale_method = st.selectbox("スケーリング手法", ["StandardScaler", "MinMaxScaler"], key="fe_scale_method")
    if st.button("スケーリング実行", key="fe_scale_btn"):
        import src.logic.feature_engineering as feature
        if scale_method == "StandardScaler":
            st.session_state['df'] = feature.standard_scale(st.session_state['df'], col4)
        else:
            st.session_state['df'] = feature.minmax_scale(st.session_state['df'], col4)
        st.success("スケーリングを実行しました")

    st.subheader("日付特徴量抽出")
    if date_cols:
        col5 = st.selectbox("日付特徴量を抽出する列", date_cols, key="fe_date_col")
        if st.button("日付特徴量抽出実行", key="fe_date_btn"):
            import src.logic.feature_engineering as feature
            st.session_state['df'] = feature.extract_date_features(st.session_state['df'], col5)
            st.success("日付特徴量を抽出しました")


def render_data_preview_with_header_input(df: pd.DataFrame, key_prefix: str = "preview") -> pd.DataFrame:
    """データプレビューと、ヘッダがない場合に手動で列名を入力できるUIを提供する。
    戻り値はプレビュー用に列名が反映された DataFrame。セッションに `preview_df` を保存する。
    """
    st.subheader("列名の確認")
    # 簡易的なヘッダ推定: 現在のカラム名に 'Unnamed' が含まれているか、整数の RangeIndex であればヘッダなしとみなす
    cols = df.columns
    likely_header = not any(str(c).startswith("Unnamed") for c in cols) and not all(isinstance(c, (int,)) for c in cols)
    use_header = st.checkbox("1行目を列名として使う", value=likely_header, key=f"{key_prefix}_use_header")

    if use_header:
        # もし現在のカラムが自動付与の整数インデックスやUnnamedの場合、先頭行をヘッダに昇格する
        if any(str(c).startswith("Unnamed") for c in cols) or all(isinstance(c, (int,)) for c in cols):
            if df.shape[0] >= 1:
                df2 = df.copy()
                df2.columns = df2.iloc[0].astype(str)
                df2 = df2.iloc[1:].reset_index(drop=True)
            else:
                df2 = df.copy()
        else:
            df2 = df.copy()
        st.dataframe(df2.head(10))
        st.session_state['preview_df'] = df2
        # プレビューで先頭行をヘッダに昇格した場合、メインの df も更新して他タブ（EDA等）に反映する
        st.session_state['df'] = df2
        return df2

    # ヘッダなしモード: ユーザーに列名を入力させる
    num_cols = df.shape[1]
    st.info("列名がないデータとして扱います。各列の名前を入力してください。")
    default_names = [f"column_{i+1}" for i in range(num_cols)]

    # プレビュー表示用: チェックがOFFの時点で仮の列名を付けて表示する
    df_preview = df.copy()
    df_preview.columns = default_names
    st.dataframe(df_preview.head(10))

    # 入力欄の初期値は既にセッションにある user_column_names を優先
    existing = st.session_state.get('user_column_names')
    initial_names = existing if existing and len(existing) == num_cols else default_names

    names = []
    cols_ui = st.columns(3)
    for i in range(num_cols):
        col_ui = cols_ui[i % 3]
        key_name = f"{key_prefix}_col_{i}"
        init_val = st.session_state.get(key_name, initial_names[i])
        val = col_ui.text_input(f"列{i+1}", value=init_val, key=key_name)
        names.append(val or default_names[i])

    pasted = st.text_area("カンマまたは改行で列名をまとめて貼り付け（任意）", key=f"{key_prefix}_paste")
    if pasted:
        pasted_list = [x.strip() for x in re.split(r"[,\n\r]+", pasted) if x.strip()]
        if len(pasted_list) == num_cols:
            names = pasted_list
            for i, n in enumerate(names):
                st.session_state[f"{key_prefix}_col_{i}"] = n
        else:
            st.warning("貼り付けた列名の数が列数と一致しません。")

    # バリデーション
    if len(set(names)) != len(names):
        st.error("列名が重複しています。異なる名前を入力してください。")

    apply_btn = st.button("列名を適用", key=f"{key_prefix}_apply")
    if apply_btn and len(set(names)) == len(names):
        df2 = df.copy()
        df2.columns = names
        st.session_state['user_column_names'] = names
        st.session_state['preview_df'] = df2
        # 適用時はメインの df も更新しておく
        st.session_state['df'] = df2
        st.success("列名を適用しました。プレビューとメインデータを更新しました。")
        st.dataframe(df2.head(10))
        return df2

    # 適用していない場合は仮のプレビューをセッションにセット
    st.session_state['preview_df'] = df_preview
    return df_preview
