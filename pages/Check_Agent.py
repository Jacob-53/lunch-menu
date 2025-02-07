import streamlit as st
from lunch_menu.db import get_connection, insert_menu, chek_agents

st.set_page_config(page_title="입력 안한 요원 찾기", page_icon="🕵")

st.title("입력 안한 요원 찾기")
st.markdown("# 누가 입력 안 했을까요?") 
st.sidebar.header("입력 안한 요원 찾기")

cdt = st.date_input("조회 할 날짜")
checkPress = st.button("입력 안 한 요원 누구냐?")
checkagent=chek_agents(cdt)
if checkPress:
   st.success(checkagent)
    
