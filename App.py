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
                "INSERT INTO lunch_menu (menu_name,member_id,dt) VALUES (%s,%s,%s);",
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
cdt = st.date_input("조회 할 날짜")
chekPress = st.button("입력 안 한 요원 누구냐?")
queryy = """
select
    m.name,
    count(l.id) as menc
from
	member m
left join lunch_menu l
on 
	l.member_id = m.id and l.dt = %s
group by
	m.id, m.name
having 
	count(l.id) = 0
order by
	menc desc
"""
if chekPress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(queryy,(cdt,))
        rowss = cursor.fetchall()
        fdf=pd.DataFrame(rowss,columns=['name','count'])
        sunsinagents=fdf['name'].tolist()
        if len(sunsinagents) >=1:
            #st.text(",  ".join(sunsinagents))
            cursor.close()
            conn.close()
            st.success(",  ".join(sunsinagents))
        else:
            cursor.close()
            conn.close()
            st.warning("모든 요원 입력 완료!")
    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")

st.subheader("Result check")
#query = "select menu_name as menu,member_id as ename,dt from lunch_menu order by dt desc"
query="""SELECT 
    lunch_menu.menu_name AS menu, 
    member.name AS ename, 
    lunch_menu.dt 
FROM member
INNER JOIN lunch_menu ON member.id = lunch_menu.member_id
ORDER BY lunch_menu.dt DESC"""

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()


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

onePress = st.button("한방에 인서트")

if onePress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        df = pd.read_csv('note/menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], var_name='dt', value_name='menu')

        sdf=mdf.replace(["-","x","<결석>"], pd.NA)
        adf=sdf.dropna()
        blm = []
        
        members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}
        success_cnt = 0
        fail_cnt = 0

        for i in adf.index: 
            ename = adf.loc[i, "ename"]
            dt = adf.loc[i, "dt"]
            value = adf.loc[i, "menu"]
            blm.append((value,members[ename],dt))
    
        cursor.executemany("INSERT INTO lunch_menu (menu_name,member_id,dt) VALUES (%s,%s,%s) ON CONFLICT (member_id,dt)  DO NOTHING",blm)
        
        success_cnt = cursor.rowcount
        fail_cnt = len(blm) - success_cnt
        
        if success_cnt == len(blm):
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"벌크 인서트 완료 총 {success_cnt} 건")
        
        else:
            st.warning(f"총 {len(blm)} 건 중 {fail_cnt} 건 실패")       
            conn.commit()
            cursor.close()
            conn.close()
    
    except Exception as e: 
        conn.rollback()
        cursor.close()
        conn.close()
        st.error(f"오류 발생 ; {e} ")
        print(f"Exception: {e}")
