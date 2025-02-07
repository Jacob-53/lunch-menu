import pandas as pd
import psycopg
import os
from dotenv import load_dotenv

load_dotenv

DB_CONFIG = { "dbname": os.getenv("DB_NAME"),                                    "user":os.getenv("DB_USERNAME"),                                      "password":os.getenv("DB_PASSWORD"),                                  "host":os.getenv("DB_HOST"),                                          "port":os.getenv("DB_PORT")                                         
 }

def get_connection():                                                     return psycopg.connect(**DB_CONFIG)

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

def select_table():
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
        
    return selected_df
 

       # df = pd.read_csv('note/menu.csv')

        #start_idx = df.columns.get_loc('2025-01-07')
        #mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], var_name='dt', value_name='menu')

        #sdf=mdf.replace(["-","x","<결석>"], pd.NA)
        #adf=sdf.dropna()
        #gdf=adf.groupby('ename')['menu'].count().reset_index()

        #gdf=selected_df.groupby('ename')['menu'].count().reset_index()
