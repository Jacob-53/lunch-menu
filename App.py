import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = { "dbname": os.getenv("DB_NAME"),
            #"user": st.secret["db_username"],
             "user":os.getenv("DB_USERNAME"),
             "password":os.getenv("DB_PASSWORD"),
             "host":os.getenv("DB_HOST"),
             "port":os.getenv("DB_PORT")
            }
members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}
def get_connection():
    return psycopg.connect(**DB_CONFIG)

conn = get_connection()
cursor = conn.cursor()

def insert_menu(menu_name,member_id,dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO lunch_menu (menu_name,member_name,dt) VALUES (%s,%s,%s);",
                   (menu_name,member_id,dt)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"Exception : {e}")
        return False

st.title("점심 뭐 먹었나요?")

st.write("""### **Let's grab a bite and then finish this up** """)

st.subheader("입력")
menu_name= st.text_input("메뉴 이름", placeholder="예: 참치김밥")
member_name =  st.selectbox(
    "누가 먹었나요?",
    options=list(members.keys()),
    index=list(members.keys()).index('jacob'),placeholder="누가 먹었나요?",
)
st.write("점심 먹은 사람은",member_name)
member_id = members[member_name]
dt = st.date_input("언제 먹었나요?")

isPress = st.button("Save data")
if isPress:
    if menu_name and member_id and dt:
        if insert_menu(menu_name,member_id,dt):
           st.success(f"입력 성공")
        else:
            st.error(f"입력 실패")
    else:
        st.warning(f"모든 값을 입력하세요")

st.subheader("Result check")
query = "select menu_name as menu,member_name as ename,dt from lunch_menu order by dt desc"

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()


selected_df = pd.DataFrame(rows,columns=['menu','ename','dt'])
selected_df

df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

sdf=mdf.replace(["-","x","<결석>"], pd.NA)
adf=sdf.dropna()
#gdf=adf.groupby('ename')['menu'].count().reset_index()

gdf=selected_df.groupby('ename')['menu'].count().reset_index()
gdf
try:
    fig, ax = plt.subplots()
    gdf.plot(x='ename',y='menu',kind='bar',ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다")
    print(f"Exception: {e}")

st.subheader("벌크 인서트")
isPress = st.button("한방에 인서트")

if isPress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        df = pd.read_csv('note/menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], var_name='dt', value_name='menu')

        sdf=mdf.replace(["-","x","<결석>"], pd.NA)
        adf=sdf.dropna()
        blm = []
        for i in adf.index: 
            ename = adf.loc[i, "ename"]
            dt = adf.loc[i, "dt"]
            value = adf.loc[i, "menu"]
            blm.append((value,ename,dt))
    
        cursor.executemany("INSERT INTO lunch_menu (menu_name,member_name,dt) VALUES (%s,%s,%s)",blm)
        conn.commit()
        cursor.close()
        conn.close()
        st.success("벌크 인서트 완료")
    except Exception as e: 
        conn.rollback()
        cursor.close()
        conn.close()
        st.error("데이터가 중복되어 실행을 취소합니다")
        print(f"Exception: {e}")
