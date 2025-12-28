import streamlit as st
import uuid
from src.ui import sidebar
from src.logic import data_io

def main() -> None:
    """
    機械学習データ前処理アプリ main.py
    - データ入出力、EDA、クリーニング、特徴量作成、エクスポートの各タブUI
    - st.session_stateによる状態・履歴管理
    """
    # セッション状態初期化
    if 'df' not in st.session_state:
        st.session_state['df'] = None
    if 'file_name' not in st.session_state:
        st.session_state['file_name'] = ''
    if 'history' not in st.session_state:
        st.session_state['history'] = []  # 各処理の履歴（コード生成用）
    # セッション固有の識別子（キャッシュ分離に使用）
    if 'session_uid' not in st.session_state:
        st.session_state['session_uid'] = str(uuid.uuid4())

    st.set_page_config(page_title="データ前処理アプリ", layout="wide")
    st.title("機械学習データ前処理アプリ")

    # サイドバー：ファイルアップロード
    uploaded = sidebar.sidebar_file_uploader()

    if uploaded is not None:
        try:
            # ファイルは毎回再読み込みすると、ユーザーが行った変換（列名変更など）が失われる。
            # そのため、以下の条件のいずれかでのみ再読込する:
            # - セッションに df が存在しない
            # - アップロードされたファイル名が前回読み込んだものと異なる
            need_load = False
            if st.session_state.get('df') is None:
                need_load = True
            elif st.session_state.get('file_name') != uploaded.name:
                need_load = True

            if need_load:
                # 常に先頭行をヘッダとして読み込む
                header_opt = 0
                if uploaded.name.endswith('.csv'):
                    df = data_io.load_csv(uploaded, header=header_opt, session_id=st.session_state['session_uid'])
                    hist_str = f"df = pd.read_csv('{uploaded.name}', header=0)"
                    st.session_state['history'].append(hist_str)
                elif uploaded.name.endswith('.parquet'):
                    df = data_io.load_parquet(uploaded, session_id=st.session_state['session_uid'])
                    st.session_state['history'].append(f"df = pd.read_parquet('{uploaded.name}')")
                else:
                    st.error("対応していないファイル形式です")
                    df = None
                st.session_state['df'] = df
                st.session_state['file_name'] = uploaded.name
        except Exception as e:
            st.session_state['df'] = None
            st.error(f"データ読み込みエラー: {e}")

    # サイドバー：データサイズ表示
    sidebar.sidebar_data_shape(st.session_state['df'])

    # サイドバー：リセットボタン
    if sidebar.sidebar_reset_button():
        st.session_state['df'] = None
        st.session_state['file_name'] = ''
        st.session_state['history'] = []
        # Streamlit のバージョン差異に備え、互換的に再実行を試みる
        try:
            st.experimental_rerun()
        except AttributeError:
            try:
                from streamlit.runtime.scriptrunner import RerunException
                raise RerunException()
            except Exception:
                try:
                    from streamlit.runtime.scriptrunner.script_runner import RerunException as _Rerun
                    raise _Rerun()
                except Exception:
                    # 最悪の場合は実行を停止して再実行を促す
                    st.stop()

    # サイドバー：ダウンロードボタン
    if st.session_state['df'] is not None:
        try:
            csv_bytes = data_io.export_csv(st.session_state['df'])
            sidebar.sidebar_download_button(
                label="CSVダウンロード",
                data=csv_bytes,
                file_name="processed.csv",
                mime="text/csv"
            )
            parquet_bytes = data_io.export_parquet(st.session_state['df'])
            sidebar.sidebar_download_button(
                label="Parquetダウンロード",
                data=parquet_bytes,
                file_name="processed.parquet",
                mime="application/octet-stream"
            )
        except Exception as e:
            st.error(f"エクスポートエラー: {e}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "データプレビュー", "EDA（探索的データ分析）", "クリーニング", "特徴量作成", "エクスポート"])

    with tab1:
        st.header("データプレビュー")
        if st.session_state['df'] is not None:
            import src.ui.forms as forms
            forms.render_data_preview_with_header_input(st.session_state['df'], key_prefix="main_preview")
        else:
            st.info("サイドバーからデータファイルをアップロードしてください")

    with tab2:
        st.header("EDA（探索的データ分析）")
        df = st.session_state['df']
        if df is not None:
            import src.logic.eda as eda
            import src.ui.charts as charts
            st.subheader("基本統計量")
            st.dataframe(eda.describe_basic(df))

            st.subheader("欠損値情報")
            st.dataframe(eda.missing_info(df))

            st.subheader("分布の可視化")
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if num_cols:
                col = st.selectbox("ヒストグラム/箱ひげ図を表示する列を選択", num_cols, key="eda_numcol")
                charts.plot_histogram(df, col)
                charts.plot_box(df, col)
            else:
                st.info("数値列がありません")

            st.subheader("相関分析")
            corr = eda.corr_matrix(df)
            st.dataframe(corr)
            charts.plot_corr_heatmap(corr)
        else:
            st.info("データをアップロードしてください")

    with tab3:
        st.header("クリーニング")
        df = st.session_state['df']
        if df is not None:
            import src.logic.cleaning as cleaning
            import src.ui.forms as forms
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            obj_cols = df.select_dtypes(include=['object']).columns.tolist()
            cat_cols = df.select_dtypes(include=['category']).columns.tolist()
            date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
            forms.cleaning_form(df, num_cols, obj_cols, cat_cols, date_cols)
            # フォーム操作で `st.session_state['df']` が更新される可能性があるため
            # 最新の DataFrame をセッションから取得してプレビュー表示する
            df = st.session_state.get('df', df)
            st.dataframe(df)
        else:
            st.info("データをアップロードしてください")

    with tab4:
        st.header("特徴量作成")
        df = st.session_state['df']
        if df is not None:
            import src.logic.feature_engineering as feature
            import src.ui.forms as forms
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            obj_cols = df.select_dtypes(include=['object']).columns.tolist()
            cat_cols = df.select_dtypes(include=['category']).columns.tolist()
            date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
            forms.feature_engineering_form(df, num_cols, obj_cols, cat_cols, date_cols)
            # フォームでエンコーディング等を実行すると `st.session_state['df']` が更新されるため
            # 最新の DataFrame を取得してプレビュー表示する
            df = st.session_state.get('df', df)
            st.dataframe(df)
        else:
            st.info("データをアップロードしてください")


    with tab5:
        st.header("エクスポート")
        df = st.session_state['df']
        if df is not None:
            import src.logic.codegen as codegen
            import src.ui.export as export
            code = codegen.generate_code(st.session_state.get('history', []))
            export.code_export_area(code)
            export.data_export_area(df)
        else:
            st.info("データをアップロードしてください")


if __name__ == "__main__":
    main()
