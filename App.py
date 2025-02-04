import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg



DB_CONFIG = { "dbname": "sunsindb",
             "user":"sunsin",
             "password":"mysecretpassword",
             "host":"localhost",
             "port":"5432"
            }

def get_connection():
    return psycopg.connect(**DB_CONFIG)

conn = get_connection()
cursor = conn.cursor()



st.title("점심 뭐 먹었나요?")

st.write("""### **Let's grab a bite and then finish this up** """)

st.subheader("입력")
menu_name= st.text_input("메뉴 이름", placeholder="예: 참치김밥")
member_name = st.text_input("먹은 사람", value="jacob")
dt = st.date_input("먹은날짜")

isPress = st.button("Save data")
if isPress:
    if menu_name and member_name and dt:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lunch_menu (menu_name,member_name,dt) VALUES (%s,%s,%s);",
               (menu_name,member_name,dt)
        )
        conn.commit()
        cursor.close()
        st.success(f"버튼{isPress}:{menu_name},{member_name},{dt}")
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

fig, ax = plt.subplots()
gdf.plot(x='ename',y='menu',kind='bar',ax=ax)
st.pyplot(fig)

st.subheader("벌크인서트")
isPress = st.button("한방에 인서트")

if isPress:
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
    st.success(f"벌크 인서트 완료")
