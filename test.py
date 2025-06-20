import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai
import os

st.title('데이터 분석 웹앱')

# --- AI 챗봇 (사이드바) ---
st.sidebar.title('AI 챗봇')
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
if openai_api_key:
    user_question = st.sidebar.text_area('질문을 입력하세요')
    if st.sidebar.button('질문하기') and user_question.strip():
        with st.spinner('AI가 답변을 생성 중입니다...'):
            try:
                openai.api_key = openai_api_key
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": user_question}]
                )
                answer = response['choices'][0]['message']['content']
                st.sidebar.success(answer)
            except Exception as e:
                st.sidebar.error(f"에러 발생: {e}")
else:
    st.sidebar.info('OpenAI API Key를 입력하면 AI 챗봇을 사용할 수 있습니다.')

# 1. CSV 파일 업로드
uploaded_file = st.file_uploader('CSV 파일을 업로드하세요', type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('데이터 미리보기')
    st.dataframe(df.head())

    # 2. 전처리: 결측치 처리
    st.subheader('결측치 처리')
    if df.isnull().sum().sum() > 0:
        if st.button('결측치 모두 제거'):
            df = df.dropna()
            st.success('결측치가 제거되었습니다.')
            st.dataframe(df.head())
    else:
        st.write('결측치가 없습니다.')

    # 3. 컬럼 선택
    st.subheader('컬럼 선택')
    selected_columns = st.multiselect('분석할 컬럼을 선택하세요', df.columns.tolist(), default=df.columns.tolist())
    df_selected = df[selected_columns]
    st.dataframe(df_selected.head())

    # 4. 시각화
    st.subheader('데이터 시각화')
    plot_type = st.selectbox('시각화 종류를 선택하세요', ['히스토그램', '상관관계 히트맵', '박스플롯'])
    if plot_type == '히스토그램':
        col = st.selectbox('히스토그램을 그릴 컬럼을 선택하세요', df_selected.select_dtypes(include='number').columns)
        fig, ax = plt.subplots()
        sns.histplot(df_selected[col], kde=True, ax=ax)
        st.pyplot(fig)
    elif plot_type == '상관관계 히트맵':
        fig, ax = plt.subplots()
        corr = df_selected.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
    elif plot_type == '박스플롯':
        col = st.selectbox('박스플롯을 그릴 컬럼을 선택하세요', df_selected.select_dtypes(include='number').columns)
        fig, ax = plt.subplots()
        sns.boxplot(y=df_selected[col], ax=ax)
        st.pyplot(fig)
else:
    st.info('먼저 CSV 파일을 업로드하세요.')
