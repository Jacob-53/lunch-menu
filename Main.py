import streamlit as st
import time
from lunch_menu.db import get_connection, insert_menu, select_table, menu_plot, today_agents, chek_agents
from datetime import datetime

st.set_page_config(page_title="점심 Check!! 뭐 먹었나요?", page_icon="🍱")
st.title("점심 뭐 먹었나요?")
st.markdown("### Let's grab a bite and then finish this up") 
_left, mid, _right = st.columns(3)

st.sidebar.header("점심 뭐 먹었나요?")
st.markdown("**순신샵 맴버들의 점심메뉴를 확인 할 수 있습니다**")
st.markdown(''' :rainbow[좌측메뉴를 선택하면] **:red[순신샵 맴버]들의 :blue[점심메뉴]를 확인 할 수 있습니다**''')
with mid:
    st.image("./src/images/donut-simpson.gif", caption=None, use_container_width=True) 
