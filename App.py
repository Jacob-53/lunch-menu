import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("점심 뭐 먹었나요?")

st.subheader("입력")
menu_name= st.text_input("메뉴 이름", placeholder="예: 참치김밥")
member_name = st.text_input("먹은 사람", value="jacob")
dt = st.date_input("먹은날짜")

st.write("""# **Let's grab a bite and then finish this up** """)

df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

sdf=mdf.replace(["-","x","<결석>"], pd.NA)
adf=sdf.dropna()
gdf=adf.groupby('ename')['menu'].count().reset_index()

gdf

fig, ax = plt.subplots()
gdf.plot(x='ename',y='menu',kind='bar',ax=ax)
st.pyplot(fig)


