import streamlit as st
from lunch_menu.db import get_connection, insert_menu, select_table, menu_plot


st.set_page_config(page_title="점심 Check!! 뭐 먹었나요?", page_icon="🍱")

st.title("점심 뭐 먹었나요?")
st.markdown("# Let's grab a bite and then finish this up")
imageurl= https://patchesofpride.wordpress.com/wp-content/uploads/2016/04/homerdoughnuts.png
st.image(imageurl, use_column_width=True)
st.sidebar.header("점심 뭐 먹었나요?")
