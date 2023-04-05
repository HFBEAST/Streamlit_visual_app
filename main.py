import pandas as pd
import yfinance as yf
import streamlit as st
import altair as alt

st.title('US company stock visualization')
st.sidebar.write("""
    # GAFA 株価
    #### こちらは株価可視化ツールです。
    #### 以下のオプションから表示日数を指定できます。
    """)

st.sidebar.write("""
    #
    ## 表示日数の指定
    """)

days = st.sidebar.slider('日数:', 1, 50, 10)

st.sidebar.write("""
    ## 株価の範囲指定
    """)

y_min, y_man = st.sidebar.slider(
    '表示範囲を選択してください:',
    0.0, 3500.0, (0.0, 3500.0))

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

company_tag = {
    'apple': 'AAPL',
    'facebook': 'META',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN',
}

# 処理スビートを軽くするため
# st.cache is deprecated. Please use one of Streamlit's new caching commands, st.cache_data or st.cache_resource.
@st.cache_data
def get_data(days, company_tag):
    df = pd.DataFrame()
    for company in company_tag.keys():
        cmp = yf.Ticker(company_tag[company])
        Data = cmp.history(period=f'{days}d')
        Data.index = Data.index.strftime('%d %B %Y')
        Data = Data[['Close']]
        Data.columns = [company]
        Data = Data.T
        Data.index.name = 'Name'
        df = pd.concat([df, Data])
    return df

df = get_data(days, company_tag)

companys = st.multiselect(
    ' 表示の会社名を選択してください。',
    list(df.index),
    ['google','apple']  # defult
)

if not companys:
    st.error('少なくとも一社は選んでください。')
else:
    data = df.loc[companys]
    st.write(" ### 株価（USD）", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date']).rename(
        columns={'value': 'Stock Prices(USD)'}
    )
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[y_min, y_man])),
            color='Name:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)


