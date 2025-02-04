import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.write("""
# It's my first app
## 밥이 좋아  **Let's grab a bite and then finish this up**

""")

df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

sdf=mdf.replace(["-","x","<결석>"], pd.NA)
adf=sdf.dropna()
gdf=adf.groupby('ename')['menu'].count().reset_index()

fig, ax = plt.subplots()
gdf.plot(x='ename',y='menu',kind='bar',ax=ax)
st.pyplot(fig)


