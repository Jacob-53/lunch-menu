import streamlit as st
import time
from lunch_menu.db import get_connection, insert_menu, select_table, menu_plot, today_agent


st.set_page_config(page_title="점심 Check!! 뭐 먹었나요?", page_icon="🍱")
st.subheader("**오늘 점심 미입력자**")

return_text = today_agent()
display_area = st.empty()
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
while True:
    for color in colors:
        display_area.markdown(
                f'<h1 style="color:{color}; text-align:center;">{return_text}</h1>',
                unsafe_allow_html=True
        )
        #st.subheader(sub_text)
        time.sleep(0.5)

st.title("점심 뭐 먹었나요?")
st.markdown("### Let's grab a bite and then finish this up") 
_left, mid, _right = st.columns(3)
with mid:
    st.image("./src/images/donut-simpson.gif", caption=None, use_container_width=True) 
st.sidebar.header("점심 뭐 먹었나요?")
st.markdown("**순신샵 맴버들의 점심메뉴를 확인 할 수 있습니다**")
st.markdown(''' :rainbow[좌측메뉴를 선택하면] **:red[순신샵 맴버]들의 :blue[점심메뉴]를 확인 할 수 있습니다**''')
