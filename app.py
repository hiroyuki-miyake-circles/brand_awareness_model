# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# 警告メッセージを非表示にする
st.set_option('deprecation.showfileUploaderEncoding', False)

# ページの設定
st.set_page_config(page_title="認知予測モデルシミュレーター", page_icon="📈")

# 係数の定義
coef = {
    'Seasonality': 2710,
    '認知費(円)': 0.0001229,
    '指名検索費(円)': 0.00244,
    '記事掲載数': 33.85,
    'intercept': 37556
}

# サイドバーの説明
st.sidebar.markdown("""
### 認知予測モデルシミュレーター

このアプリでは、以下の入力値から認知予測モデルによるブランドキーワードクリック数を予測します。

- 予測月
- 認知費
- 指名検索費
- 記事掲載数

入力値を変更すると、リアルタイムで予測値が更新されます。詳細は入力フィールドのツールチップを参照してください。
""")

# メインコンテンツ
st.title("認知予測モデルシミュレーター")

# 入力フォーム
with st.form("input_form"):
    st.header("入力値")
    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "予測月",
            options=["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"],
            help="予測対象の月を選択してください。"
        )

    with col2:
        pm_awareness = st.number_input(
            "認知費(円)",
            value=0,
            step=100000,
            format="%d",
            help="認知費の金額を入力してください。"
            )
        
        sem_investment = st.number_input(
            "指名検索費(円)",
            value=0,
            step=100000,
            format="%d",
            help="指名検索費の金額を入力してください。"
        )

        publications = st.number_input(
            "記事掲載数",
            value=0,
            step=100,
            format="%d",
            help="記事掲載数を入力してください。"
        )
        

    submitted = st.form_submit_button("予測実行")

if submitted:
    # 予測実行
    with st.spinner("予測を実行しています..."):
        # 季節性の計算
        uq2019_options = {
            "January": 109,
            "February": 109,
            "March": 118,
            "April": 100,
            "May": 95,
            "June": 88,
            "July": 89,
            "August": 77,
            "September": 110,
            "October": 96,
            "November": 85,
            "December": 90
        }
        uq2019 = uq2019_options[selected_month]
        seasonality_contribution = round(coef['Seasonality'] * uq2019 + coef['intercept'],1)
        awareness_contribution = round(coef['認知費(円)'] * pm_awareness,1)
        sem_brand_contribution = round(coef['指名検索費(円)'] * sem_investment,1)
        publications_contribution = round(coef['記事掲載数'] * publications,1)

        # 予測値の計算
        predicted_value = round(
            seasonality_contribution +
            awareness_contribution +
            sem_brand_contribution +
            publications_contribution,
            1
        )

        predicted_GAvalue = round(predicted_value * 0.0221, 1)
        
        # 各変数のGA寄与値を計算し、小数点第1位まで丸める
        seasonality_GA_contribution = round((coef['Seasonality'] * uq2019 + coef['intercept']) * 0.0221, 1)
        awareness_GA_contribution = round((coef['認知費(円)'] * pm_awareness) * 0.0221, 1)
        sem_brand_GA_contribution = round((coef['指名検索費(円)'] * sem_investment) * 0.0221, 1)
        publications_GA_contribution = round((coef['記事掲載数'] * publications) * 0.0221, 1)

    # 結果の表示
    st.header("予測結果")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "予測ブランドキーワードクリック数",
            f"{predicted_value:,.0f} click",
            delta=None,
            delta_color="normal"
        )

    with col2:
        st.metric(
            "予測GA",
            f"{predicted_GAvalue:,.1f} GA",
            delta=None,
            delta_color="normal"
        )

    st.header("詳細")
    with st.expander("詳細を表示"):
        st.write(f'ベース認知 : {seasonality_contribution:.1f} click = {seasonality_GA_contribution:.1f} GA')
        st.write(f'認知費 : {awareness_contribution:.1f} click = {awareness_GA_contribution:.1f} GA')
        st.write(f'指名検索費 : {sem_brand_contribution:.1f} click = {sem_brand_GA_contribution:.1f} GA')
        st.write(f'記事掲載数 : {publications_contribution:.1f} click = {publications_GA_contribution:.1f} GA')

        # 結果の可視化
        data = {
            '要因': ['ベース認知', '認知費', '指名検索費', '記事掲載数'],
            '寄与値': [
                seasonality_contribution,
                awareness_contribution,
                sem_brand_contribution,
                publications_contribution
            ],
            'GA寄与値': [
                seasonality_GA_contribution,
                awareness_GA_contribution,
                sem_brand_GA_contribution,
                publications_GA_contribution
            ]
        }
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index('要因')['寄与値'])
        st.bar_chart(df.set_index('要因')['GA寄与値'])

    # レポートのダウンロード
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        "レポートをCSVでダウンロード",
        csv,
        "report.csv",
        "text/csv",
        key='download-csv'
    )
