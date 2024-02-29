# -*- coding: utf-8 -*-
"""認知モデルStreamlit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zWlTzyHZQJlZHrmbn17PXUDOfwB7TWC-
"""

import streamlit as st

# アプリのタイトル
st.title('認知予測モデルシミュレーター')

# 係数の定義
coef = {
    'Seasonality': 3336,
    '認知費(円)': 0.000451762526,
    '指名検索費(円)': 0.00359574998,
    '記事掲載数': 52.1965121,
    'intercept': -104174
}

# UQ2019の選択肢
uq2019_options = {
    'January': 109,
    'February': 114,
    'March': 169,
    'April': 100,
    'May': 88,
    'June': 69,
    'July': 72,
    'August': 77,
    'September': 102,
    'October': 76,
    'November': 85,
    'December': 96
}

# ユーザー入力
selected_month = st.selectbox('予測月を選択してください', list(uq2019_options.keys()))
uq2019 = uq2019_options[selected_month]
pm_awareness = st.number_input('認知費(円)', value=0.0, format='%f')
sem_investment = st.number_input('指名検索費(円)', value=0.0, format='%f')
publications = st.number_input('記事掲載数', value=0.0, format='%f')

# 予測実行ボタン
if st.button('run'):
     # 各変数の寄与値を計算
    seasonality_contribution = coef['Seasonality'] * uq2019 + coef['intercept']
    awareness_contribution = coef['認知費(円)'] * pm_awareness
    sem_brand_contribution = coef['指名検索費(円)'] * sem_investment
    publications_contribution = coef['記事掲載数'] * publications

    # 予測計算
    predicted_value = (
        seasonality_contribution +
        awareness_contribution +
        sem_brand_contribution +
        publications_contribution
    )

    # 予測値の表示
    st.write(f'予測brand keyword click: {predicted_value}')
    st.write('---詳細---')
    st.write(f'ベース認知 click: {seasonality_contribution}')
    st.write(f'認知費 click: {awareness_contribution}')
    st.write(f'指名検索費 click: {sem_brand_contribution}')
    st.write(f'記事掲載数 click: {publications_contribution}')

