import sqlite3
import google.generativeai as genai
import streamlit as st
import os
import pandas as pd
from test_prompt import prompt
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))

def  get_gemini_response(question,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0],question])
    return response.text

def read_sql_query(sql, db,start_time):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    if len(rows) == 0:
        st.write("The result is empty")
    elif len(rows) > 1 or len(rows[0]) > 1:
        columns = [description[0] for description in cur.description]
        data = pd.DataFrame(rows, columns=columns)
        st.dataframe(data)
        end = datetime.now()
        st.write(f"time required:{(end.second)-(start_time.second)} sec.")
    else:
        st.write(rows[0][0])
        end = datetime.now()
        st.write(f"time required:{(end.second)-(start_time.second)} sec.")
    conn.commit()
    conn.close()
    return rows



st.set_page_config(page_title="AI Analytics")

st.markdown("<style>.my-title{font-family:'serif';text-align: center;color:black;}</style>",unsafe_allow_html=True,)
st.markdown(f'<h1 class="my-title">Rewardola Analytics with AI</h1>',unsafe_allow_html=True)

# sidebar image
st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] > div:first-child {{
        background: url("https://images.pexels.com/photos/13786121/pexels-photo-13786121.jpeg")left;
        background-size:cover;
    }}
    </style>
    """,
    unsafe_allow_html=True,
    )


# st.markdown(
#     f"""
#     <style>
#     [data-testid="stSidebar"] > div:first-child {{
#         background-color : #e2e4e5;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True,
#     )


# Instructions
with st.sidebar:
    st.markdown("<style>.sidebar-title{font-family:'Cambria';text-align:center;color:#47524a;}</style>",unsafe_allow_html=True,)
    st.markdown(f'<h2 class="sidebar-title">INSTRUCTIONS</h2>',unsafe_allow_html=True)
    st.markdown("""
◼ Start by clearly typing your question related to the data you're interested in.
\n◼ If your question is about specific data, include the table name; mention it in your query.
\n◼ Once the app generates results, take your time to go through the information presented. Results are derived based on your query parameters, so careful examination is key.
\n◼ Note that results might not always be 100% accurate. Variations can occur due to the complexity of data or the specificity of your question.
\n◼ If results are not as expected, consider rephrasing your question. Making your prompt simpler or more detailed, especially with date-related queries, can significantly impact the accuracy and relevance of the results.
\nHappy Analyzing! Dive in and start exploring your data.""")



# bg image
st.markdown(
f"""
<style>
.stApp {{
    background: url("https://images.pexels.com/photos/965119/pexels-photo-965119.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1") center;
    background-size:cover;
}}
</style>
""",
unsafe_allow_html=True,
)


question=st.text_input("**Query**", placeholder="Ask Question About Your Data.", key='input')
submit=st.button('**Ask**')



if submit and question:
    start  = datetime.now()
    response = get_gemini_response(question, prompt)
    res = response.split("```")
    query = (res[1].removeprefix("sql\n")).removesuffix("\n")
    logic = (res[2].removeprefix("\n\n")).removesuffix("\n")
    st.write("**SQL Query :**",query)
    st.write("\n")
    st.write(logic)
    st.write("\n")
    st.write("**The Response is:**")
    data = read_sql_query(query, "rewardola1.db",start)
    print("SQL Query:",query)
    print("Logic & Explaination:",logic)